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

if not os.path.isdir('dataset'):
    print("Error, could not find dataset folder")
    exit()

AUTOTUNE = tf.data.experimental.AUTOTUNE

# Set default number of epochs for training cycle
EPOCHS = 50
# Change batch size to higher number
BATCH_SIZE = 1
IMG_HEIGHT = 360
IMG_WIDTH = 640

# Check if testing and training directories already exists
if os.path.isdir('dataset/testing') and os.path.isdir('dataset/training'):
    data_dir = pathlib.Path("dataset/training")
    # Count number of images for doing training
    image_count = len(list(data_dir.glob("*/*.jpg")))
    CLASS_NAMES = np.array([item.name for item in data_dir_temp.glob("*") if item.name != '.DS_Store'])
else:
    data_dir = pathlib.Path("dataset")
    image_count = len(list(data_dir.glob("*/*.jpg")))
    CLASS_NAMES = np.array([item.name for item in data_dir.glob("*") if item.name != '.DS_Store'])
    # Create testing and training directories
    os.mkdir("dataset/testing")
    os.mkdir("dataset/training")
    # Create class directories in testing folder
    for class in CLASS_NAMES:
        os.mkdir("dataset/testing/" + class)
    # Move random 1/10th of photos of each map to testing directory
    for class in CLASS_NAMES:
        class_path = pathlib.Path("dataset/" + class)
        dir_count = len(list(class_path.glob("*.jpg")))
        for x in range(dir_count//10):
            option = choice(os.listdir(str(class_path)))
            src = "dataset/" + class + "/" + option
            dst = "dataset/testing/" + option
            shutil.move(src, dst)
    # Move class directories into training folder
    for class in CLASS_NAMES:
        shutil.move("dataset/" + class, "dataset/training/" + class)
    # Reset data directory and image count
    data_dir = pathlib.Path("dataset/training")
    image_count = len(list(data_dir.glob("*/*.jpg")))

STEPS_PER_EPOCH = np.ceil(image_count/BATCH_SIZE)

list_train_ds = tf.data.Dataset.list_files(str(data_dir/'*/*.jpg'))
test_dir = "dataset/testing"
list_test_ds = tf.data.Dataset.list_files(test_dir + "/*/*.jpg")


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
    img = tf.image.decode_jpeg(img, channels=3)
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    img = tf.image.convert_image_dtype(img, tf.float32)
    # resize the image to the desired size.
    return tf.image.resize(img, [IMG_WIDTH, IMG_HEIGHT])

def process_path(file_path):
    label = get_label(file_path)
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
        period=5)

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
model.load_weights(checkpoint_path)

optlist, args = getopt.getopt(sys.argv[1:], ['help', 'epochs', 'batch', 'load', 'eval', 'train'])
for option, arg in optlist:
    if option == '--help':
        print("Usage:\n --epochs [number epochs]\n --batch [batch size]\n --eval\n   Evaluates images in test directory and prints accuracy\n --train\n   Fits loaded model to training data using batch size and number of epochs")
    if option == '--epochs':
        EPOCHS = int(arg)
    if option == '--batch':
        BATCH_SIZE = int(arg)
    if option == '--eval':
        results = model.evaluate(test_ds)
        print('test loss, test acc:', results)
    if arg == '--train':
        history = model.fit(train_ds, verbose=1, epochs=EPOCHS, callbacks=[cp_callback], validation_data=test_ds)
