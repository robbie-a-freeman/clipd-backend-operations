import tensorflow as tf

from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

import sys
import os

# IMPORT AND SET IMAGES HERE
# All images should be imported here, training and testing data
(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

# SET PATH VARIABLE FOR SAVING MODEL
checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Callback for setting checkpoints
# Will resave weights every 5 epochs (period)
cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path,
    verbose=1,
    save_weights_only=True,
    period=5)

# SET NUMBER OF EPOCHS FOR EACH TRAINING CYCLE
EPOCHS = 50

# NORMALIZE INPUT IMAGES
train_images, test_images = train_images / 255.0, test_images / 255.0

class_names = ['inferno', 'dust_2', 'mirage', 'cache', 'nuke', 'train', 'vertigo']


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

for arg in sys.argv[1:]:
    if arg == 'load':
        model.load_weights(checkpoint_path)
    if arg == 'eval':
        loss, acc = model.evaluate(test_images, test_labels)
        # Print out results here
    if arg == 'train':
        history = model.fit(train_images, train_labels, verbose=1, epochs=EPOCHS, callbacks=[cp_callback], validation_data=(test_images, test_labels))
