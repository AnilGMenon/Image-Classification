#Description: This program classifies images

#Import the libraries
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras import layers
from tensorflow.keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

from keras.datasets import cifar10
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

#Look at the datatypes of the variables
print(type(x_train))
print(type(y_train))
print(type(x_test))
print(type(y_test))

#Get the shape of the arrays
print('x_train shape: ', x_train.shape)
print('y_train shape: ', y_train.shape)
print('x_test shape: ', x_test.shape)
print('y_test shape: ', y_test.shape)

#Take a look at the first image as an array
index = 10
x_train[index]

#Show the image as a picture
img = plt.imshow(x_train[index])

#Get the image label
print('Ther image label is: ', y_train[index])

#Get the image classification
classification = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
#Print the image class
print('The image class is:', classification[y_train[index][0]])

#Convert the labels into set of 10 numbers to input into the neural network
y_train_one_hot = to_categorical(y_train)
y_test_one_hot = to_categorical(y_test)

#Print the new labels
print(y_train_one_hot)

#Print the new label of the image above
print('The one hot lable is: ', y_train_one_hot[index])

#Normalize the pixesl to be values between 0 and 1
x_train = x_train / 255
x_test = x_test /255

x_train[index]

#Create the models architecture (Nueral Network Architecture)
model = Sequential()

#Add the first layer
model.add(Conv2D(32, (5, 5), activation='relu', input_shape= (32,32,3)))

#Add a pooling layer
model.add(MaxPooling2D(pool_size=(2,2)))

#Add another convolution layer
model.add(Conv2D(32, (5, 5), activation='relu'))

#Add another pooling layer
model.add(MaxPooling2D(pool_size=(2,2)))

#Add a flattening layer. Reduces it to a linear array
model.add(Flatten())

#Add a layer with 1000 neurons
model.add(Dense(1000, activation='relu'))

#Add a dropout layer
model.add(Dropout(0.5))

#Add a layer with 500 neurons
model.add(Dense(500, activation='relu'))

#Add a dropout layer
model.add(Dropout(0.5))

#Add a layer with 250 neurons
model.add(Dense(250, activation='relu'))

#Add a layer with 10 neurons
model.add(Dense(10, activation='softmax'))

#Compile the model
model.compile(loss = 'categorical_crossentropy',
              optimizer = 'adam',
              metrics = ['accuracy'])

#Train the model
hist = model.fit(x_train, y_train_one_hot, 
                 batch_size = 256, 
                 epochs=10,
                 validation_split = 0.2)

#Evaluate the model using the test data set
model.evaluate(x_test, y_test_one_hot)[1]

#Visualize the models accurary
plt.plot(hist.history['accuracy'])
plt.plot(hist.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc='upper left')
plt.show()

#Visualize the models loss
plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc='upper right')
plt.show()

#Test the model with an example
from google.colab import files
uploaded = files.upload()

#Show the image
new_img = plt.imread('deer.jpeg')
img= plt.imshow(new_img)

#Resize the image
from skimage.transform import resize
resized_image = resize(new_img, (32,32,3))
img = plt.imshow(resized_image)

#Model predicting the image (Model Predictions)
predictions = model.predict(np.array([resized_image]))
#Show predicitions
predictions

#Sort the predictions from least to greatest
list_index = [0,1,2,3,4,5,6,7,8,9]
x = predictions

for i in range(10):
  for j in range(10):
    if x[0][list_index[i]] > x[0][list_index[j]]:
      temp = list_index[i]
      list_index[i] = list_index[j]
      list_index[j] = temp

#Show the sorted labels in order
print(list_index)

#Print the first 5 predictions

for i in range(5):
  print(classification[list_index[i]], ':', round(predictions[0][list_index[i]] * 100, 2), '%')