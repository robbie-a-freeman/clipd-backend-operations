import keyboard
#from collections import deque 
import time
import winsound
from threading import Thread
from queue import Queue
from PIL import ImageGrab
from PIL import Image
from PIL import ImageChops
from PIL import ImageStat

# threading code
class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                # An exception happened in this thread
                print(e)
            finally:
                # Mark this task as done, whether an exception happened or not
                self.tasks.task_done()


class ThreadPool:
    """ Pool of threads consuming tasks from a queue """
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """ Add a task to the queue """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """ Add a list of tasks to the queue """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """ Wait for completion of all the tasks in the queue """
        self.tasks.join()


# Assumes a demo is open, paused, in counterstrike, a player being spectated, at the beginning

# initialize variables
# Need to check these
NUMBER_OF_TICKS = 505148
MAP_NAME = 'de_vertigo'
TICKS_PER_GAME_SECOND = 128 # any professional demo
playersToSkip = [] #list(range(1,9))
#PATH = 'C:/Users/zaroh/OneDrive/Documents/GitHub/clipd-backend/data'
PATH = 'E:'

# Should stay the same
NUMBER_OF_PLAYERS = 10
SCREENSHOTS_PER_GAME_SECOND = 3
NUMBER_OF_THREADS = 30
IMAGE_SIZE = (640, 360)
TIME_TO_PLAY_BEFORE_PAUSE = 0.3
currentScreenshot = 0

#screenshotsToProcess = deque()

# wait 10 seconds to alt+tab back to csgo window, beep after time
time.sleep(5.0)
winsound.Beep(1000, 100)
pool = ThreadPool(NUMBER_OF_THREADS)

# save to disk
def writeToDisk(p, i):
    print('writing', i)
    p = p.resize(IMAGE_SIZE)
    p.save(PATH + '/' + MAP_NAME + '/' + MAP_NAME + '_' + str(i) + '.png', "PNG")

def isPixelGray(p):
    p0_1 = abs(p[0] - p[1])
    p1_2 = abs(p[1] - p[2])
    p0_2 = abs(p[0] - p[2])
    if p0_1 <= 5 and p0_2 <= 5 and p1_2 <= 5 and p[0] > 30 and p[0] < 225: # not white or black
        return True
    else:
        return False

def checkIfSmoke(img):
    tlPixel = img.getpixel( (img.width / 4, img.height / 4) )
    trPixel = img.getpixel( (3 * img.width / 4, img.height / 4) )
    blPixel = img.getpixel( (img.width / 4, 3 * img.height / 4) )
    brPixel = img.getpixel( (3 * img.width / 4, 3 * img.height / 4) )
    if isPixelGray(tlPixel) and isPixelGray(trPixel) and isPixelGray(blPixel) and isPixelGray(brPixel):
        print("Skipping ahead to avoid smoke bug")
        return True
    return False

# takes the mean of each picture's set of pixels and compares them
def identical(p1, p2):
    p1Mean = ImageStat.Stat(p1).mean
    p2Mean = ImageStat.Stat(p2).mean
    p1_2x = abs(p1Mean[0] - p2Mean[0])
    p1_2y = abs(p1Mean[1] - p2Mean[1])
    p1_2z = abs(p1Mean[2] - p2Mean[2])
    if p1_2x <= 0.2 and p1_2y <= 0.2 and p1_2z <= 0.2:
        return True
    else:
        return False

# ahk binds used for j (start vod at 0), k (skip 42 ticks), and nums

keyboard.press_and_release('j')
currentTick = 0
lastImage = Image.new('RGB', (1, 1))
# until the end of the demo
while currentTick < NUMBER_OF_TICKS:
    # for each player, record screenshots throughout the vod
    for p in range(NUMBER_OF_PLAYERS):
        # check if players are to be skipped
        if p in playersToSkip:
            continue
        else:
            time.sleep(0.05) # so that we dont skip things
            keyboard.press_and_release(str(p))
        # take the screenshot, send to thread to be saved
        printscreen_pil = ImageGrab.grab()
        if checkIfSmoke(printscreen_pil): # account for demo smoke bug and possible dupes
            keyboard.press_and_release('=') # play at 1x for 0.5 seconds
            time.sleep(TIME_TO_PLAY_BEFORE_PAUSE) 
            keyboard.press_and_release('.') # pause again
            currentTick =  currentTick + int(TIME_TO_PLAY_BEFORE_PAUSE * TICKS_PER_GAME_SECOND) # lose some screenshots, but I think that's negligible
        elif identical(lastImage, printscreen_pil):
            print(ImageStat.Stat(printscreen_pil).mean)
            print(ImageStat.Stat(lastImage).mean)
            print("identical image not recorded")
        else:
            #screenshotsToProcess.appendleft(printscreen_pil)
            pool.add_task(writeToDisk, printscreen_pil, currentScreenshot)
            currentScreenshot = currentScreenshot + 1
        lastImage = printscreen_pil
    # advance to next time
    keyboard.press_and_release('k')
    currentTick = 42 + currentTick
            