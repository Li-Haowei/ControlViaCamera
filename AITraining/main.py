import cv2
import os
import numpy as np
import shutil
import imageio
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout


# get the current working directory
cwd = os.getcwd()
cwd+='\AITraining'

# Source of the dataset: https://www.idiap.ch/webarchives/sites/www.idiap.ch/resource/gestures/
# Jochen Triesch Static Hand Posture Database

# get the path to the hand_dataset folder
dataset_dir = os.path.join(cwd, 'hand_dataset')

# Load the images and labels
data = []
labels = []
counter = 0
for item in os.listdir(dataset_dir):
    item_path = os.path.join(dataset_dir, item)
    if os.path.isfile(item_path) and item.endswith('.pnm'):
        # Item is a file containing an image
        image = imageio.imread(item_path)
        if image.ndim == 2:
            image = np.expand_dims(image, axis=-1)
        image = np.divide(image, 255.0)  # Normalize pixel values to [0, 1]
        data.append(image)
        counter += 0.001
        labels.append(counter)
    elif os.path.isdir(item_path):
        # Item is a directory containing images
        for image_file in os.listdir(item_path):
            image_path = os.path.join(item_path, image_file)
            if os.path.isfile(image_path) and image_file.endswith('.pnm'):
                image = imageio.imread(image_path)
                if image.ndim == 2:
                    image = np.expand_dims(image, axis=-1)
                image = np.divide(image, 255.0)  # Normalize pixel values to [0, 1]
                data.append(image)
                labels.append(item)

# Convert the data and labels to numpy arrays
data = np.array(data)
labels = np.array(labels)

# Use data and labels to train a model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(62, 58, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(10, activation='softmax'))
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# model.fit(data, labels, epochs=10), Case String to float is not supported
data = data.astype('float32')
# output labels into a file
np.savetxt('labels.txt', labels, fmt='%s')
# labels = labels.astype('float32')
model.fit(data, labels, epochs=10)

# Save the model
model.save(os.path.join(cwd, 'hand_model'))