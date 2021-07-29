import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import os
import random
import joblib

from xgboost import XGBClassifier
from time import time, sleep, strftime, gmtime
from sklearn.model_selection import train_test_split
from muselsl import stream, list_muses, record
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
from EEG_generate_training_matrix_realtime import gen_training_matrix

""" Real-time Minecraft State Classification """
if __name__ == "__main__":

    # eeg_samples = []
    # timestamps = []

    # def save_eeg(new_samples, new_timestamps):
    #     eeg_samples.append(new_samples)
    #     timestamps.append(new_timestamps)

    # muse = Muse(address, save_eeg, backend=backend)
    # muse.connect()
    # muse.start()

    
    """ Obtain the real-time signal values """
    
    muses = list_muses()

    streams = resolve_byprop('type', 'EEG', timeout=2)
    chunk_length = 12
    if len(streams) == 0:
        raise RuntimeError('Can\'t find EEG stream.')

    print("Started acquiring data.")
    inlet = StreamInlet(streams[0], max_chunklen=chunk_length)
    eeg_time_correction = inlet.time_correction()

    info = inlet.info()
    description = info.desc()

    Nchan = info.channel_count()

    ch = description.child('channels').first_child()
    ch_names = [ch.child_value('label')]
    for i in range(1, Nchan):
        ch = ch.next_sibling()
        ch_names.append(ch.child_value('label'))

    # Get the sampling frequency
    # This is an important value that represents how many EEG data points are
    # collected in a second. This influences our frequency band calculation.
    # for the Muse 2016, this should always be 256
    fs = int(info.nominal_srate())

    """ Set it to 5 seconds for testing currently """
    duration = 5
    eeg_samples = []
    timestamps = []
    t_init = time()
    time_correction = inlet.time_correction()
    last_written_timestamp = None
    print('Start recording at time t=%.3f' % t_init)
    # print('Time correction: ', time_correction)

    """ Change this while loop to true """
    while (time() - t_init) < duration:
        try:
            data, timestamp = inlet.pull_chunk(
                timeout=1.0, max_samples=chunk_length)

            if timestamp:
                eeg_samples.append(data)
                timestamps.extend(timestamp)
                tr = time()
            
        except KeyboardInterrupt:
            break
    
    eeg_samples = np.concatenate(eeg_samples, axis=0)
    timestamps = np.array(timestamps) + time_correction

    eeg_samples = np.c_[timestamps, eeg_samples]
    data = pd.DataFrame(data=eeg_samples, columns=["timestamps"] + ch_names)
    np_data = np.array(data)
    print('data{}: \n{}'.format(np_data.shape, np_data))
    matrix = gen_training_matrix(np_data, [])
    print('matrix generated!')
    print('matrix{}:\n{}'.format(matrix.shape, matrix))

    # time_correction = inlet.time_correction()
    # print("Time correction: ", time_correction)



    """ Minecraft State Classification """
    
    """ 1. Load the pre-trained model """
    model = tf.keras.models.load_model(os.getcwd() + '/saved_models/minecraft-state-c-gru.h5')
    # model = joblib.load(open(os.getcwd() + '/saved_models/xgb.joblib', 'rb'))

    """ 2. Make the raw prediction """
    raw_pred = model.predict(matrix)
    
    print('raw_pred: ')
    print(raw_pred)

    """ 2. Interpret into readable result """
    pred_arr = np.array(list(map(lambda x: np.argmax(x), raw_pred)))

    print('pred_arr: ')
    print(pred_arr)

    counts = np.bincount(pred_arr)
    state_num = np.argmax(counts)

    if state_num == 2:
        print('Building')
    elif state_num == 1:
        print('Mining')
    elif state_num == 0:
        print('Wandering')
    
