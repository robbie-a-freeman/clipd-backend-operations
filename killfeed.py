from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
import numpy as np
import string
import matplotlib.pyplot as plt

# Set the path of the tesseract installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

DEBUG = False
icon_dir = 'icons/guns/'
test_dir = 'data/test/'
screenshot = test_dir + 'screenshots/0.png'

# My measured ratio for how large the icon should be in the image
RATIO = 1/15
THRESH = 0.8

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

# For grouping multiple close matching templates
def groups(first,second):
    group = []
    assert first.size == second.size
    cur_group_x = -20
    cur_group_y = -20
    for i in range(first.size):
        if abs(second[i] - cur_group_y) > 1:
            cur_group_x = first[i]
            cur_group_y = second[i]
            # Swap order because OpenCV swaps width and height
            group.append((cur_group_y, cur_group_x))
        else:
            cur_group_x = first[i]
            cur_group_y = second[i]
    return group

if DEBUG:
    first = np.array([95,95,95,95,95,95])
    second = np.array([1,2,3,5,5,8])
    print(groups(first,second))

def process_tag(image):
    im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, im = cv2.threshold(im,210,255,cv2.THRESH_BINARY)
    im = 255 - im
    return im

# Takes in an image path
def process_killfeed(image_path):
    image = cv2.imread(image_path)
    height, width, channels = np.shape(image)
    height_quarter = int(height/4)
    width_quarter = int(width/4)
    # Get upper right corner of image and process
    image_upper = image[:height_quarter, width-width_quarter:]
    #print('image_upper size:', np.shape(image_upper))
    image_grayed = cv2.cvtColor(image_upper, cv2.COLOR_BGR2GRAY)
    ret, threshed = cv2.threshold(image_grayed,190,255,cv2.THRESH_BINARY)
    if DEBUG:
        cv2.imshow('cropped', image_upper)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # Calculate guessed icon height
    icon_height = int(height_quarter*RATIO)
    killfeed = []
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
            cv2.destroyAllWindows()
        # Find icon in processed image
        res = cv2.matchTemplate(threshed, resized_icon, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= THRESH)
        if DEBUG and loc[0].size > 0:
            top_left = groups(*loc)[0]
            bottom_right = (top_left[0] + icon_width, top_left[1] + icon_height)
            #print(top_left, bottom_right)
            img = image_upper.copy()
            cv2.rectangle(img, top_left, bottom_right, 255, 2)
            cv2.imshow(name, img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        for top_left in groups(*loc):
            #print(top_left)
            killer_tag = image_upper[top_left[1]-3:top_left[1]+icon_height+5, :top_left[0]]
            dead_tag = image_upper[top_left[1]-3:top_left[1]+icon_height+5, top_left[0]+icon_width+2:]
            killer_tag = process_tag(killer_tag)
            dead_tag = process_tag(dead_tag)
            killer_text = pytesseract.image_to_string(killer_tag)
            dead_text = pytesseract.image_to_string(dead_tag)
            if DEBUG:
                cv2.imshow('killer tag', killer_tag)
                cv2.waitKey(0)
                cv2.imshow('dead tag', dead_tag)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                print(killer_text)
                print(dead_text)
            # TO DO: Check for headshot/wallbang
            killfeed.append((killer_text, name, dead_text))
    return killfeed
        


print(process_killfeed(screenshot))