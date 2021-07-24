import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import os
import random

from sklearn.model_selection import train_test_split
from muselsl import stream, list_muses
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import utils  # Our own utility functions

""" EXPERIMENTAL PARAMETERS """
# Modify these to change aspects of the signal processing

# Length of the EEG data buffer (in seconds)
# This buffer will hold last n seconds of data and be used for calculations
BUFFER_LENGTH = 5

# Length of the epochs used to compute the FFT (in seconds)
EPOCH_LENGTH = 1

# Amount of overlap between two consecutive epochs (in seconds)
OVERLAP_LENGTH = 0.8

# Amount to 'shift' the start of each next consecutive epoch
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

# Index of the channel(s) (electrodes) to be used
# 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
INDEX_CHANNEL = [0]

if __name__ == "__main__":

    """ 1. CONNECT TO EEG STREAM """

    # Search for active LSL streams
    print('Looking for an EEG stream...')
    streams = resolve_byprop('type', 'EEG', timeout=2)
    if len(streams) == 0:
        raise RuntimeError('Can\'t find EEG stream.')

    # Set active EEG stream to inlet and apply time correction
    print("Start acquiring data")
    inlet = StreamInlet(streams[0], max_chunklen=12)
    eeg_time_correction = inlet.time_correction()

    # Get the stream info and description
    info = inlet.info()
    description = info.desc()

    # Get the sampling frequency
    # This is an important value that represents how many EEG data points are
    # collected in a second. This influences our frequency band calculation.
    # for the Muse 2016, this should always be 256
    fs = int(info.nominal_srate())

    """ 2. INITIALIZE BUFFERS """

    # Initialize raw EEG data buffer
    eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
    filter_state = None  # for use with the notch filter

    # Compute the number of epochs in "buffer_length"
    n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) /
                              SHIFT_LENGTH + 1))

    # Initialize the band power buffer (for plotting)
    # bands will be ordered: [delta, theta, alpha, beta]
    band_buffer = np.zeros((n_win_test, 4))

""" 3. GET DATA """

# The try/except structure allows to quit the while loop by aborting the
# script with <Ctrl-C>
print('Press Ctrl-C in the console to break the while loop.')

try:
    # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
    while True:

        """ 3.1 ACQUIRE DATA """
        # Obtain EEG data from the LSL stream
        eeg_data, timestamp = inlet.pull_chunk(
            timeout=1, max_samples=int(SHIFT_LENGTH * fs))

        # print('eeg_data: \n')
        # print('Shape: {}'.format(np.array(eeg_data).shape))
        # print(eeg_data)


        # Only keep the channel we're interested in
        ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]

        # Update EEG buffer with the new data
        eeg_buffer, filter_state = utils.update_buffer(
            eeg_buffer, ch_data, notch=True,
            filter_state=filter_state)

        print('eeg_buffer:')
        print('Shape: {}'.format(eeg_buffer.shape))
        print(eeg_buffer)

except KeyboardInterrupt:
    print('Closing!')







model = tf.keras.models.load_model(os.getcwd() + '/saved_models/1246_gru.h5')

# model.summary()

# 1246_gru: Test Accuracy: 50.714%
# # 1246_gru_test: Test Accuracy: 91.429%
outfile_path = os.getcwd() + '/final_dataset/mental-state-test.csv'
mental_state_test = pd.read_csv(outfile_path)

# 1246_gru: Test Accuracy: 92.742%
# 1246_gru_test: Test Accuracy: 68.414%
# outfile_path = os.getcwd() + '/final_dataset/mind_wandering.csv'
# mind_wandering = pd.read_csv(outfile_path)

def preprocess_inputs(df):
    df = df.copy()

    y = df['Label'].copy()
    X = df.drop('Label', axis=1).copy()

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=123)

    return X_train, X_test, y_train, y_test


X_train, X_test, y_train, y_test = preprocess_inputs(mental_state_test)

model_acc = model.evaluate(X_test, y_test, verbose=0)[1]
print("Test Accuracy: {:.3f}%".format(model_acc * 100))
