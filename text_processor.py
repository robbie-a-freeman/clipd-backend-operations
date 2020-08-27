import pytesseract
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Set the path of the tesseract installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
DEBUG = True

# Attempts to seperate image into 2 clusters based on pixel similarity, returns masked image
def k_means(img):
    Z = img.reshape((-1,3))
    # convert to np.float32
    Z = np.float32(Z)
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 2
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    # Now convert back into uint8, and make original image
    center = np.array([0, 255], dtype=np.uint8)
    #center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape[:-1]))
    return res2

def sharpen(img):
    f = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img = cv2.filter2D(img,-1,f)
    return img

def to_gray(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def threshold_range(img, thresh_range=(190, 240, 3)):
    results = []
    for thresh in range(*thresh_range):
        ret, threshed = cv2.threshold(img,thresh,255,cv2.THRESH_BINARY)
        results.append(threshed)
    return results

def process_text(img, check_database = False):
    # to do: try expanding image dimensions (pixelating)
    gray = to_gray(img)
    filters = threshold_range(gray)
    filters.append(k_means(img))
    filters.append(sharpen(k_means(img)))
    possible_outputs = []
    for x in filters:
        text = pytesseract.image_to_string(x)
        possible_outputs.append(text)
    if DEBUG:
        i = 0
        for x in filters:
            cv2.imshow('f'+str(i), x)
            i+=1
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # to do: remove empty strings and check remaining strings against database
    return possible_outputs