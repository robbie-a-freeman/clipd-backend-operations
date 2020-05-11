import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import sys
from random import choice
import os
import shutil
import pathlib
import numpy as np
import getopt

try:
    print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
except:
    print("Error finding GPUs")
#tf.config.gpu.set_per_process_memory_fraction(0.75)
#tf.config.gpu.set_per_process_memory_growth(False)
physical_devices = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_visible_devices(physical_devices[0], 'GPU')
try:
    #tf.config.experimental.set_virtual_device_configuration(physical_devices[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=4096)])

    from tensorflow.compat.v1 import ConfigProto
    from tensorflow.compat.v1 import InteractiveSession
    config = ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 0.75
    config.gpu_options.allow_growth = True
    #tf.compat.v1.RunOptions(report_tensor_allocations_upon_oom = True)
    session = InteractiveSession(config=config)

    #tf.config.experimental.set_memory_growth(physical_devices[0], True) 
    print("Successfully limiting GPU memory growth")
except: 
    # Invalid device or cannot modify virtual devices once initialized. 
    print("Error limiting GPU memory growth")

AUTOTUNE = tf.data.experimental.AUTOTUNE

# Change batch size to higher number
BATCH_SIZE = 10
IMG_HEIGHT = 360
IMG_WIDTH = 640

def decode_imgs(file_path):
    files = pathlib.Path(file_path).glob("*.png")
    decoded = []
    for x in files:
        img = tf.io.read_file(x)
        img = decode_img(img)
        # convert the compressed string to a 3D uint8 tensor
        img = tf.image.decode_png(img, channels=3)
        # Use `convert_image_dtype` to convert to floats in the [0,1] range.
        img = tf.image.convert_image_dtype(img, tf.float32)
        # resize the image to the desired size.
        img = tf.image.resize(img, [IMG_WIDTH, IMG_HEIGHT])
        decoded.append(img)
    return decoded
    
def most_frequent(List): 
    return max(set(List), key = List.count) 

# SET PATH VARIABLE FOR SAVING MODEL
checkpoint_path = "modelCheckpoints/cp.ckpt"

class_names = ['inferno', 'dust_2', 'mirage', 'cache', 'nuke', 'train', 'vertigo']

def create_model():
    model = models.Sequential()
    model.add(layers.Conv2D(120, (10, 10), activation='relu', input_shape=(640,360,3)))
    model.add(layers.AveragePooling2D((5, 5)))
    model.add(layers.Conv2D(240, (10, 10), activation='relu'))
    model.add(layers.AveragePooling2D((5, 5)))
    model.add(layers.Conv2D(240, (10, 10), activation='relu'))


    model.add(layers.Flatten())
    model.add(layers.Dense(240, activation='relu'))
    model.add(layers.Dense(7, activation='softmax')) # softmax makes all answers add up to one

    try:
        model.load_weights(checkpoint_path)
    except:
        print("Error loading weights")
        exit()

    return model

model = create_model()

optlist, args = getopt.getopt(sys.argv[1:], 'h', ['eval'])
for option, arg in optlist:
    if option == '--eval':
        images = decode_imgs(arg)
        output = model(images)
        outs = []
        for x in output:
            outs.append(tf.argmax(x))
        print(most_frequent(outs))
    elif option == '-h':
        print("Usage:\n --eval [directory]")
session.close()
