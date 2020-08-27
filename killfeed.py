import cv2
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from text_processor import process_text

# TO DO: Check for headshot/wallbang
#      : Fix text detection

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

if DEBUG and False:
    print(format_name('102_icon-m4a1.png.png'))

os_dir = os.listdir(icon_dir)
icons = [cv2.imread(icon_dir + x) for x in os_dir]
names = [format_name(x) for x in os_dir]

if DEBUG and False:
    cv2.imshow(names[0], icons[0])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# takes 2 numpy arrays and returns a list of pairs
def zip_numpy(first,second):
    group = []
    assert first.size == second.size
    for i in range(first.size):
        group.append((first[i], second[i]))
    return group

if DEBUG and False:
    first = np.array([95,95,95,95,95,95])
    second = np.array([1,2,3,5,5,8])
    print(zip_numpy(first,second))

def crop_tags(cropped_image, top_left, icon_size):
    killer_tag = cropped_image[top_left[0]-5 : top_left[0]+icon_size[0]+7, :top_left[1]+9]
    dead_tag = cropped_image[ top_left[0]-5 : top_left[0]+icon_size[0]+7, top_left[1]+icon_size[1]-9:]
    if DEBUG:
        cv2.imshow('killer tag', killer_tag)
        cv2.imshow('dead tag', dead_tag)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return killer_tag, dead_tag

# Returns True if first location and second location are as close as half the icon size
def near(first, second, icon_size):
    if abs(first[0] - second[0]) < icon_size[0] // 2 and abs(first[1] - second[1]) < icon_size[1] // 2:
        return True
    return False

def swap(a,b):
    return (b,a)

def resize_icon(icon, target_height):
    # Set icon height
    ic_h, ic_w = icon.shape
    ratio = target_height / ic_h
    reshaped_width = int(ic_w * ratio)
    resized_icon = cv2.resize(icon, (reshaped_width, target_height))
    if DEBUG and False:
        cv2.imshow('resized icon', resized_icon)
        cv2.waitKey(0)
    return resized_icon

def find_icons(cropped_image, ratio_range=(10, 30, 2)):
    # Proprocess image to find icon
    image_grayed = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    ret, threshed = cv2.threshold(image_grayed,190,255,cv2.THRESH_BINARY)
    if DEBUG and False:
        cv2.imshow('threshed', threshed)
        cv2.waitKey(0)
    # Search through all icons, with different ratios, recording % matches
    height, width, _ = np.shape(cropped_image)
    found_icons = []
    for ratio in range(*ratio_range):
        icon_height = height // ratio
        for icon, name in zip(icons, names):
            icon = cv2.cvtColor(icon, cv2.COLOR_BGR2GRAY)
            icon_resized = resize_icon(icon, icon_height)
            resized_width, resized_height = icon_resized.shape
            # Find icon in processed image
            res = cv2.matchTemplate(threshed, icon_resized, cv2.TM_CCOEFF_NORMED)
            # Get location of found icons (% match) above a threshold
            loc = np.where(res >= THRESH)
            # For each location match, check if icon already found near it
            for top_left in zip_numpy(*loc):
                if DEBUG and False:
                    bottom_right = (top_left[0] + resized_width, top_left[1] + resized_height)
                    print('Found icon', name, res[top_left])
                    img = cropped_image.copy()
                    cv2.rectangle(img, swap(*top_left), swap(*bottom_right), 255, 2)
                    cv2.imshow(name, img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                failed = False
                for found in found_icons:
                    (_, match_percent, top_left_, icon_space) = found
                    # If match % is > an already found icon, replace it
                    if near(top_left, top_left_, icon_space) and res[top_left] > match_percent:
                        found_icons.remove(found)
                        break
                    elif near(top_left, top_left_, icon_space):
                        failed = True
                        break
                # If failed == True, an icon has been found that already has a high match percent
                if not failed:
                    found_icons.append((name, res[top_left], top_left, (resized_width, resized_height)))
    return found_icons

def get_killfeed(cropped_image, found_icons):
    killfeed = []
    for (gun, match, top_left, icon_half_size) in found_icons:
        kill_tag, death_tag = crop_tags(cropped_image, top_left, icon_half_size)
        killfeed.append((kill_tag, gun, death_tag))
    return killfeed

# Takes in an image path
def process_killfeed(image_path):
    image = cv2.imread(image_path)
    height, width, channels = np.shape(image)
    height_slice = int(height/2)
    width_slice = int(width/5)
    # Get upper right corner of image and process
    image_upper = image[:height_slice, width-width_slice:]
    found_icons = find_icons(image_upper)
    killfeed = get_killfeed(image_upper, found_icons)
    text_feed = []
    for (kill_tag, gun, death_tag) in killfeed:
        kill_text = process_text(kill_tag)
        death_text = process_text(death_tag)
        text_feed.append((kill_text, gun, death_text))
    return text_feed

#print(process_killfeed(screenshot))
import glob
import pathlib
screenshots_path = 'data/test/'
screenshots = pathlib.Path(screenshots_path).glob("*/*.png")
for s in screenshots:
    print(str(s), process_killfeed(str(s)))