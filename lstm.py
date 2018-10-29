#from keras.models import Sequential
#from keras.layers.convolutional import Conv3D
#from keras.layers.convolutional_recurrent import ConvLSTM2D
#from keras.layers.normalization import BatchNormalization
import numpy as np
import pylab as plt
import os, re
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))
data = pd.read_csv(os.path.join(dir_path, "static", "images", "20161001_120007", "results.csv"))     # reading the csv file
data.head() # printing first five rows of the file
data.values[1].remove()

def tryint(s):
    try:
        return int(s)
    except:
        return s
def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

# We create a layer which take as input movies of shape
# (n_frames, width, height, channels) and returns a movie
# of identical shape.
dimensions = (1080, 1920, 3)
# send in a 5 second clip to determine if the point starts = 60x5 = 300
seq = Sequential()
#batch, steps, width, height, features

seq.add(ConvLSTM2D(filters=40, kernel_size=(3, 3),
                   input_shape=(None, dimensions[0], dimensions[1], dimensions[2]),
                   padding='same', return_sequences=True))
seq.add(BatchNormalization())

seq.add(ConvLSTM2D(filters=40, kernel_size=(3, 3),
                   padding='same', return_sequences=True))
seq.add(BatchNormalization())

seq.add(ConvLSTM2D(filters=40, kernel_size=(3, 3),
                   padding='same', return_sequences=True))
seq.add(BatchNormalization())

seq.add(ConvLSTM2D(filters=40, kernel_size=(3, 3),
                   padding='same', return_sequences=True))
seq.add(BatchNormalization())

seq.add(Conv3D(filters=1, kernel_size=(3, 3, 3),
               activation='relu',
               padding='same', data_format='channels_last'))
seq.compile(loss='binary_crossentropy', optimizer='adadelta')


# Artificial data generation:
# Generate movies with 3 to 7 moving squares inside.
# The squares are of shape 1x1 or 2x2 pixels,
# which move linearly over time.
# For convenience we first create movies with bigger width and height (80x80)
# and at the end we select a 40x40 window.

def generate_input_batch(start=0, n_frames=3000):
    # return images, y from the resutls.txt for the batch
    frames = []
    y_frames = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    frames = os.listdir(os.path.join(dir_path, "static", "images", "20161001_120007"))
                #print(images)
    frames.sort(key=alphanum_key)
    rPath = os.path.join(dir_path, "results.txt")
    if os.path.exists(rPath):
        with open(rPath, 'rb') as f:
            y_frames = f.read().splitlines()

    return frames, y_frames
    

# Train the network
frames, y_frames = generate_input_batch(start=0, n_frames=600)
seq.fit(frames[:1000], y_frames[:1000], batch_size=60,
        epochs=300, validation_split=0.05)

# Testing the network on one movie

