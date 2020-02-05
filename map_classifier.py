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
try:
    tf.config.experimental.set_virtual_device_configuration(physical_devices[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2048)])
    #tf.config.experimental.set_memory_growth(physical_devices[0], False) 
    print("Successfully limiting GPU memory growth")
except: 
    # Invalid device or cannot modify virtual devices once initialized. 
    print("Error limiting GPU memory growth")

if not os.path.isdir('dataset'):
    print("Error, could not find dataset folder")
    exit()

AUTOTUNE = tf.data.experimental.AUTOTUNE

# Set default number of epochs for training cycle
EPOCHS = 5
# Change batch size to higher number
BATCH_SIZE = 5
IMG_HEIGHT = 360
IMG_WIDTH = 640

# Check if testing and training directories already exists
if os.path.isdir('dataset/testing') and os.path.isdir('dataset/training'):
    print("dataset/testing and dataset/training already exist, skipping dataset move")
    data_dir = pathlib.Path("dataset/training")
    # Count number of images for doing training
    image_count = len(list(data_dir.glob("*/*.png")))
    CLASS_NAMES = np.array([item.name for item in data_dir.glob("*") if item.name != '.DS_Store'])
else:
    print("Starting dataset move")
    data_dir = pathlib.Path("dataset")
    image_count = len(list(data_dir.glob("*/*.png")))
    CLASS_NAMES = np.array([item.name for item in data_dir.glob("*") if item.name != '.DS_Store'])
    # Create testing and training directories
    print("Creating dataset/testing")
    os.mkdir("dataset/testing")
    print("Creating datatset/training")
    os.mkdir("dataset/training")
    # Create class directories in testing folder
    for name in CLASS_NAMES:
        print("Creating dataset/testing/" + name)
        os.mkdir("dataset/testing/" + name)
    # Move random 1/10th of photos of each map to testing directory
    for name in CLASS_NAMES:
        print("Starting class: " + name)
        class_path = pathlib.Path("dataset/" + name)
        dir_count = len(list(class_path.glob("*.png")))
        print("Total image count: " + str(dir_count))
        print("Moving " + str(dir_count//10) + " images")
        for x in range(dir_count//10):
            option = choice(os.listdir(str(class_path)))
            src = "dataset/" + name + "/" + option
            dst = "dataset/testing/" + name + "/" + option
            shutil.move(src, dst)
    # Move class directories into training folder
    for name in CLASS_NAMES:
        print("Moving dataset/" + name + " to dataset/training/" + name)
        shutil.move("dataset/" + name, "dataset/training/" + name)
    # Reset data directory and image count
    data_dir = pathlib.Path("dataset/training")
    image_count = len(list(data_dir.glob("*/*.png")))
    print("Finished dataset move")

data_dir_testing = pathlib.Path("dataset/testing")
image_count_testing = len(list(data_dir.glob("*/*.png")))
STEPS_PER_EPOCH_TESTING = np.ceil(image_count_testing/BATCH_SIZE)

STEPS_PER_EPOCH = np.ceil(image_count/BATCH_SIZE)

list_train_ds = tf.data.Dataset.list_files(str(data_dir/'*/*.png'))
test_dir = "dataset/testing"
list_test_ds = tf.data.Dataset.list_files(test_dir + "/*/*.png")


# Prints 5 random samples
#for f in list_train_ds.take(5):
#    print(f.numpy())

def get_label(file_path):
    # convert the path to a list of path components
    parts = tf.strings.split(file_path, os.path.sep)
    # The second to last is the class-directory
    return parts[-2] == CLASS_NAMES

def decode_img(img):
    # convert the compressed string to a 3D uint8 tensor
    img = tf.image.decode_png(img, channels=3)
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    img = tf.image.convert_image_dtype(img, tf.float32)
    # resize the image to the desired size.
    return tf.image.resize(img, [IMG_WIDTH, IMG_HEIGHT])

def process_path(file_path):
    label = get_label(file_path)
    label = tf.where(tf.equal(label, True))
    # load the raw data from the file as a string
    img = tf.io.read_file(file_path)
    img = decode_img(img)
    return img, label

labeled_train_ds = list_train_ds.map(process_path, num_parallel_calls=AUTOTUNE)
labeled_test_ds = list_test_ds.map(process_path, num_parallel_calls=AUTOTUNE)

#for image, label in labeled_train_ds.take(1):
#    print("Image shape: ", image.numpy().shape)
#    print("Label: ", label.numpy())

def prepare_for_training(ds, cache=True, shuffle_buffer_size=1000):
    # This is a small dataset, only load it once, and keep it in memory.
    # use `.cache(filename)` to cache preprocessing work for datasets that don't
    # fit in memory.
    if cache:
        if isinstance(cache, str):
            ds = ds.cache(cache)
        else:
            ds = ds.cache()
    ds = ds.shuffle(buffer_size=shuffle_buffer_size)
    # Repeat forever
    ds = ds.repeat()
    ds = ds.batch(BATCH_SIZE)
    # `prefetch` lets the dataset fetch batches in the background while the model
    # is training.
    ds = ds.prefetch(buffer_size=AUTOTUNE)
    return ds

# IMPORT AND SET IMAGES HERE
# All images should be imported here, training and testing data
train_ds = prepare_for_training(labeled_train_ds)
test_ds = prepare_for_training(labeled_test_ds)

# SET PATH VARIABLE FOR SAVING MODEL
checkpoint_path = "cp.ckpt"

# Callback for setting checkpoints
# Will resave weights every 5 epochs (period)
cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path,
        verbose=1,
        save_weights_only=True,
        period=1)

# NORMALIZE INPUT IMAGES
# train_images, test_images = train_images / 255.0, test_images / 255.0

# class_names = ['inferno', 'dust_2', 'mirage', 'cache', 'nuke', 'train', 'vertigo']


'''
plt.figure(figsize=(10,10))
for i in range(25):
  plt.subplot(5,5,i+1)
  plt.xticks([])
  plt.yticks([])
  plt.grid(False)
  plt.imshow(train_images[i], cmap=plt.cm.binary)
  plt.xlabel(class_names[train_labels[0][0]])
plt.show()
'''

def create_model():
    model = models.Sequential()
    model.add(layers.Conv2D(120, (10, 10), activation='relu', input_shape=(640,360,3)))
    model.add(layers.AveragePooling2D((5, 5)))
    model.add(layers.Conv2D(240, (10, 10), activation='relu'))
    model.add(layers.AveragePooling2D((5, 5)))
    model.add(layers.Conv2D(240, (10, 10), activation='relu'))


    model.add(layers.Flatten())
    model.add(layers.Dense(240, activation='relu'))
    model.add(layers.Dense(7, activation='softmax'))

    model.summary()

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

model = create_model()
if os.path.isfile(checkpoint_path):
    model.load_weights(checkpoint_path)

optlist, args = getopt.getopt(sys.argv[1:], 'h', ['epochs=', 'batch=', 'load', 'eval', 'train'])
for option, arg in optlist:
    if option == '-h':
        print("Usage:\n --epochs=[number epochs]\n --eval\n   Evaluates images in test directory and prints accuracy\n --train\n   Fits loaded model to training data using number of epochs\nMust manually set batch size in file")
    if option == '--epochs':
        EPOCHS = int(arg)
        STEPS_PER_EPOCH = np.ceil(image_count/BATCH_SIZE)
    if option == '--eval':
        results = model.evaluate(test_ds, steps=STEPS_PER_EPOCH_TESTING)
        print('test loss, test acc:', results)
    if option == '--train':
        history = model.fit(train_ds, verbose=1, epochs=EPOCHS, steps_per_epoch=STEPS_PER_EPOCH, callbacks=[cp_callback], validation_data=test_ds, validation_steps=STEPS_PER_EPOCH_TESTING)
