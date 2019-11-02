
'''Trains a simple convnet on the MNIST dataset.
Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''

from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import LSTM
from keras import backend as K
import numpy as np

batch_size = 128
num_classes = 10
epochs = 5

# input image dimensions
img_rows, img_cols = 28, 28

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], x_train.shape[1]))
x_test = np.reshape(x_test, (x_test.shape[0], x_train.shape[1], x_test.shape[1]))

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(LSTM(128, input_shape=(28, 28)))
model.add(Dense(10, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(x_train, y_train,batch_size=batch_size,epochs=epochs,verbose=1,validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])




'''
# Imports
import sys

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.models import load_model
import numpy as np


class MnistLSTMClassifier(object):
    def __init__(self):
        # Classifier
        self.time_steps=28 # timesteps to unroll
        self.n_units=128 # hidden LSTM units
        self.n_inputs=28 # rows of 28 pixels (an mnist img is 28x28)
        self.n_classes=10 # mnist classes/labels (0-9)
        self.batch_size=128 # Size of each batch
        self.n_epochs=5
        # Internal
        self._data_loaded = False
        self._trained = False

    def __create_model(self):
        self.model = Sequential()
        self.model.add(LSTM(self.n_units, input_shape=(self.time_steps, self.n_inputs)))
        self.model.add(Dense(self.n_classes, activation='softmax'))

        self.model.compile(loss='categorical_crossentropy',
                      optimizer='rmsprop',
                      metrics=['accuracy'])

    def __load_data(self):
        self.mnist = input_data.read_data_sets("mnist", one_hot=True)
        self._data_loaded = True

    def train(self, save_model=False):
        self.__create_model()
        if self._data_loaded == False:
            self.__load_data()

        x_train = [x.reshape((-1, self.time_steps, self.n_inputs)) for x in self.mnist.train.images]
        x_train = np.array(x_train).reshape((-1, self.time_steps, self.n_inputs))

        self.model.fit(x_train, self.mnist.train.labels,
                  batch_size=self.batch_size, epochs=self.n_epochs, shuffle=False)

        self._trained = True
        
        if save_model:
            self.model.save("./saved_model/lstm-model.h5")

    def evaluate(self, model=None):
        if self._trained == False and model == None:
            errmsg = "[!] Error: classifier wasn't trained or classifier path is not precised."
            print(errmsg, file=sys.stderr)
            sys.exit(0)

        if self._data_loaded == False:
            self.__load_data()

        x_test = [x.reshape((-1, self.time_steps, self.n_inputs)) for x in self.mnist.test.images]
        x_test = np.array(x_test).reshape((-1, self.time_steps, self.n_inputs))

        model = load_model(model) if model else self.model
        test_loss = model.evaluate(x_test, self.mnist.test.labels)
        print(test_loss)


if __name__ == "__main__":
    lstm_classifier = MnistLSTMClassifier()
    lstm_classifier.train(save_model=True)
    lstm_classifier.evaluate()
    # Load a trained model.
    #lstm_classifier.evaluate(model="./saved_model/lstm-model.h5")
'''