# -*- coding: utf-8 -*-
"""Shelly Victory_Image Classification Model Deployment

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EhEw0HToy3eGbweAQtN16A91uhWmD0xu
"""

import numpy as np
from tensorflow.keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, Activation, MaxPooling2D, Dropout
from keras.callbacks import EarlyStopping
from sklearn import preprocessing
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf

import zipfile,os
base_dir = '/content/drive/MyDrive/COVID-19_Radiography_Dataset'
os.listdir(base_dir)

classes=["COVID", "Lung_Opacity", "Normal", "Viral Pneumonia"]

train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'val')

datagen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=20,
                    horizontal_flip=True,
                    shear_range = 0.2,
                    fill_mode = 'constant',
                    validation_split=0.2)

train_generator=datagen.flow_from_directory(
    base_dir,
    target_size=(150, 150),
    color_mode='rgb',
    batch_size=4,
    class_mode='categorical',
    subset='training')

validation_generator=datagen.flow_from_directory(
    base_dir,
    target_size=(150, 150),
    color_mode='rgb',
    batch_size=4,
    class_mode='categorical',
    subset='validation')

model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2, 2),
    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(512, activation='relu'),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(4, activation='softmax'),
])

model.compile(loss='categorical_crossentropy',
              optimizer='Adam',
              metrics=['accuracy'])

early = EarlyStopping(patience=5, monitor='val_loss', mode = 'min',verbose=0)
history = model.fit(train_generator, epochs=8, validation_data=validation_generator, callbacks=[early])

import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Akurasi Model')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Loss Model')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with tf.io.gfile.GFile('model.tflite', 'wb') as f:
  f.write(tflite_model)