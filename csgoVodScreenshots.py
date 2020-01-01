import keyboard
#from collections import deque 
import time
import winsound
from threading import Thread
from queue import Queue
from PIL import ImageGrab
from PIL import Image

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
NUMBER_OF_TICKS = 1000
MAP_NAME = 'map'
TICKS_PER_GAME_SECOND = 128 # any professional demo
playersToSkip = []
# Should stay the same
NUMBER_OF_PLAYERS = 10
SCREENSHOTS_PER_GAME_SECOND = 3
PATH = 'C:/Users/Robbie/Documents/GitHub/clipd-backend/data'
NUMBER_OF_THREADS = 20
IMAGE_SIZE = (640, 360)
currentScreenshot = 0

#screenshotsToProcess = deque()
# opens csgo console assuming csgo is open, inputs command, closes it
def writeToConsole(command):
    keyboard.write('~')
    keyboard.write(command)
    keyboard.press_and_release('enter')
    keyboard.write('~')

# wait 10 seconds to alt+tab back to csgo window, beep after time
time.sleep(10.0)
winsound.Beep(1000, 100)
pool = ThreadPool(NUMBER_OF_THREADS)

# save to disk
def writeToDisk(p, i):
    print('executing', i)
    p = p.resize(IMAGE_SIZE)
    p.save(PATH + '/' + MAP_NAME + '/' + MAP_NAME + '_' + str(i) + '.png', "PNG")

# for each player, record screenshots throughout the vod
for p in range(NUMBER_OF_PLAYERS):
    # check if players are to be skipped
    if len(playersToSkip) > 0:
        if p in playersToSkip:
            continue

    writeToConsole('demo_gototick 0')
    writeToConsole('demo_pause')
    currentTick = 0
    keyboard.write(str(p)) # switch to player
    # until the end of the demo
    while currentTick < NUMBER_OF_TICKS:
        # take the screenshot, send to thread to be saved
        printscreen_pil = ImageGrab.grab()
        #screenshotsToProcess.appendleft(printscreen_pil)
        pool.add_task(writeToDisk, printscreen_pil, currentScreenshot)
        # advance to next time
        writeToConsole(' '.join(['demo_gototick', str(currentTick)]))
        currentTick = int(currentTick + TICKS_PER_GAME_SECOND / SCREENSHOTS_PER_GAME_SECOND)
        currentScreenshot = currentScreenshot + 1