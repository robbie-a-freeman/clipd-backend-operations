# Adapted from https://stackoverflow.com/questions/30136257/how-to-get-image-from-video-using-opencv-python

import cv2
import os
import pytesseract
from PIL import Image
from PIL import ImageFilter
import textdistance # for string comparison
import numpy as np

def ocr_core(image):
    """
    This function will handle the core OCR processing of images.
    """
    #im1 = im.filter(ImageFilter.BLUR)
    im = image.filter(ImageFilter.SHARPEN)
    #im.show()
    text = pytesseract.image_to_string(im)  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

# Takes in a text and evaluates whether it is alphanumeric. Supposed to filter out
# false positives from tesseract such as underscores.
def isNotEmpty(text):
    return not text.isspace() and len(text) >= 3 and text.isprintable()

# Helper function that determines whether a given frame is a frame in which the
# "Kill Feed" is updated
def getKillFeed(frame, latestKillFeed):
    #from matplotlib import cm
    im = Image.fromarray(frame.astype('uint8'), 'RGB')
    # crop the frame to the part of the screen with the kill feed
    killFeedImg = im.crop( (int(im.width * 9 / 10), 0, im.width, int(im.height / 10)) )

    # read the text
    newKillFeed = ocr_core(killFeedImg)
    return newKillFeed

# evaluates the initial frame and looks for the following information:
# - player names
# - team names
# - score
def launchState(initIm, path_output_dir):
    # find team names
    teamNames = initIm.crop( (int(im.width * 9 / 10), 0, im.width, int(im.height / 10)) )
    cv2.imwrite(os.path.join(path_output_dir, 'init.png'), initIm)



def video_to_frames(video, path_output_dir):
    # extract frames from a video and save to directory as 'x.png' where 
    # x is the frame index
    vidcap = cv2.VideoCapture(video)
    count = 0
    defeats = 0
    FRAME_COUNT = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    NUMBER_OF_SS = 10
    FRAME_INCREMENT = int(FRAME_COUNT / NUMBER_OF_SS)
    while vidcap.isOpened():
        success, image = vidcap.read()
        lastKillFeed = ''
        if success:
            # if the text is similar enough to previous knowledge of kill feed, or if text is notdiscernably present, return false
            feed = getKillFeed(image, lastKillFeed)
            if feed:
                print(feed)
                print("hamming", textdistance.hamming(lastKillFeed, feed))

            # determine whether to print image
            if count % FRAME_INCREMENT == 0:
                cv2.imwrite(os.path.join(path_output_dir, '%d.png') % count, image)
                #print("used")
            elif feed and (textdistance.hamming(lastKillFeed, feed) >= 8 and isNotEmpty(feed)):
                print("kill cap found")
                lastKillFeed = feed
                defeats = defeats + 1
                cv2.imwrite(os.path.join(path_output_dir, 'killFeed%d.png') % defeats, image)
            count += 1
        else:
            break
    cv2.destroyAllWindows()
    vidcap.release()

video_to_frames('data/test/test_clip.mp4', 'data/test/screenshots')