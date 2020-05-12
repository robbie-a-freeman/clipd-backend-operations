from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
import numpy as np
import string
import matplotlib.pyplot as plt

# TO DO: Check for headshot/wallbang
#      : Fix text detection

# Set the path of the tesseract installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

DEBUG = False
icon_dir = 'icons/guns/'
test_dir = 'data/test/'
screenshot = test_dir + 'screenshots/Screenshot.png'

# Threshold for matching an icon
THRESH = 0.85

# The icons we decompiled from CS:GO source files automatically retained the
# extra .png, which as of now we are working around.
pattern = re.compile('(.*)_icon-(.*)\.png\.png')
def format_name(filename):
    out = pattern.search(filename)
    name = out.group(2)
    return name

if DEBUG:
    print(format_name('102_icon-m4a1.png.png'))

os_dir = os.listdir(icon_dir)
icons = [cv2.imread(icon_dir + x) for x in os_dir]
names = [format_name(x) for x in os_dir]

if DEBUG:
    cv2.imshow(names[0], icons[0])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# takes 2 numpy arrays and returns a list of pairs
def groups(first,second):
    group = []
    assert first.size == second.size
    for i in range(first.size):
        group.append((first[i], second[i]))
    return group

if DEBUG:
    first = np.array([95,95,95,95,95,95])
    second = np.array([1,2,3,5,5,8])
    print(groups(first,second))

def process_tag(image):
    im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Max frequencies of shade, make 5 color for threshold
    # Threshold
    ret, im = cv2.threshold(im,120,255,cv2.THRESH_BINARY)
    # Inverse
    im = 255 - im
    if DEBUG:
        cv2.imshow('killer tag', im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return im

def crop_tags(image_upper, top_left, half_size):
    killer_tag = image_upper[top_left[0]-3:top_left[0]+(half_size[1]*2)+5, :top_left[1]+2]
    dead_tag = image_upper[top_left[0]-3:top_left[0]+(half_size[1]*2)+5, top_left[1]+(half_size[0]*2)-2:]
    
    if DEBUG:
        cv2.imshow('killer tag', killer_tag)
        cv2.waitKey(0)
        cv2.imshow('dead tag', dead_tag)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return killer_tag, dead_tag

# Returns if first distance and second distance are as close as the icon
def near(first, second, distance):
    if abs(first[0] - second[0]) < distance[0] and abs(first[1] - second[1]) < distance[1]:
        return True
    return False

# Takes in an image path
def process_killfeed(image_path):
    image = cv2.imread(image_path)
    height, width, channels = np.shape(image)
    height_slice = int(height/2)
    width_slice = int(width/5)
    # Get upper right corner of image and process
    image_upper = image[:height_slice, width-width_slice:]
    #print('image_upper size:', np.shape(image_upper))
    image_grayed = cv2.cvtColor(image_upper, cv2.COLOR_BGR2GRAY)
    ret, threshed = cv2.threshold(image_grayed,190,255,cv2.THRESH_BINARY)
    if DEBUG:
        cv2.imshow('cropped', threshed)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # Find guns in image
    guns = []
    for rat in range(20, 30):
        # Calculate icon height based on ratio
        icon_height = int(height_slice*(1/(rat)))
        for i in range(len(icons)):
            icon = icons[i]
            name = names[i]
            icon = cv2.cvtColor(icon, cv2.COLOR_BGR2GRAY)
            # Set icon to guessed height
            ic_h, ic_w = icon.shape
            ratio = icon_height / ic_h 
            icon_width = int(ic_w * ratio)
            resized_icon = cv2.resize(icon, (icon_width,icon_height))
            if DEBUG and False:
                cv2.imshow('resized icon', resized_icon)
                cv2.waitKey(0)
            # Find icon in processed image
            res = cv2.matchTemplate(threshed, resized_icon, cv2.TM_CCOEFF_NORMED)
            # Get location of found icons (% match) above a threshold
            loc = np.where(res >= THRESH)
            if DEBUG and loc[0].size > 0 and False:
                top_left = groups(*loc)[0]
                bottom_right = (top_left[0] + icon_width, top_left[1] + icon_height)
                #print(top_left, bottom_right)
                img = image_upper.copy()
                cv2.rectangle(img, top_left, bottom_right, 255, 2)
                cv2.imshow(name, img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            for top_left in groups(*loc):
                failed = False
                # Checks if the gun was already found with a higher % match. If this match is higher, replace it
                for g in guns:
                    if near(g[3], top_left, g[4]) and res[top_left] > g[2]:
                        guns.remove(g)
                        break
                    elif near(g[3], top_left, g[4]):
                        failed = True
                        break
                if not failed:
                    guns.append((name, rat, res[top_left], top_left, (int(icon_width/2),int(icon_height/2))))
    killfeed = []
    for g in guns:
        k_t, d_t = crop_tags(image_upper, g[3], g[4])
        k_tp = process_tag(k_t)
        d_tp = process_tag(d_t)
        kill_string = pytesseract.image_to_string(k_tp)
        dead_string = pytesseract.image_to_string(d_tp)
        killfeed.append((kill_string, g[0], dead_string))
    return killfeed
        


#print(process_killfeed(screenshot))
import glob
import pathlib
screenshots_path = 'data/image_evaluator_test'
screenshots = pathlib.Path(screenshots_path).glob("*/*.png")
for s in screenshots:
    print(str(s), process_killfeed(str(s)))