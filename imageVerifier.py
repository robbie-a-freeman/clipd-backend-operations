from os import listdir
from PIL import Image
import pathlib
import numpy as np
   
data_dir = pathlib.Path("dataset")
CLASS_NAMES = np.array([item.name for item in data_dir.glob("testing/*") if item.name != '.DS_Store'])
for name in CLASS_NAMES:
    print(name, 'starting')
    for filename in listdir("dataset/testing/" + name):
        if filename.endswith('.png'):
            try:
                img = Image.open('dataset/testing/'+name+'/'+filename) # open the image file
                img.verify() # verify that it is, in fact an image
            except (IOError, SyntaxError) as e:
                print('Bad file:', filename) # print out the names of corrupt files

print("done with testing, now training")

for name in CLASS_NAMES:
    print(name, 'starting')
    for filename in listdir("dataset/training/" + name):
        if filename.endswith('.png'):
            try:
                img = Image.open('dataset/training/'+name+'/'+filename) # open the image file
                img.verify() # verify that it is, in fact an image
            except (IOError, SyntaxError) as e:
                print('Bad file:', filename) # print out the names of corrupt files
