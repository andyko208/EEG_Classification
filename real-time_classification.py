import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
import random
import joblib
import time
import winsound

import commands

from xgboost import XGBClassifier
from time import time, sleep, strftime, gmtime
from sklearn.model_selection import train_test_split
from muselsl import stream, list_muses, record
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
from EEG_generate_training_matrix_realtime import gen_training_matrix

# from scipy.signal import butter, lfilter, lfilter_zi
# NOTCH_B, NOTCH_A = butter(4, np.array([55, 65]) / (256 / 2), btype='bandstop')

# def update_buffer(data_buffer, new_data, notch=False, filter_state=None):
#     """
#     Concatenates "new_data" into "data_buffer", and returns an array with
#     the same size as "data_buffer"
#     """
#     if new_data.ndim == 1:
#         new_data = new_data.reshape(-1, data_buffer.shape[1])

#     if notch:
#         if filter_state is None:
#             filter_state = np.tile(lfilter_zi(NOTCH_B, NOTCH_A),
#                                    (data_buffer.shape[1], 1)).T
#         new_data, filter_state = lfilter(NOTCH_B, NOTCH_A, new_data, axis=0,
#                                          zi=filter_state)

#     new_buffer = np.concatenate((data_buffer, new_data), axis=0)
#     new_buffer = new_buffer[new_data.shape[0]:, :]

#     return new_buffer, filter_state
# Filtering stuff
# BUFFER_LENGTH = 5
# eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
# filter_state = None


""" Real-time Minecraft State Classification """
if __name__ == "__main__":
    
    """ Obtain the real-time signal values """    
    streams = resolve_byprop('type', 'EEG', timeout=2)
    chunk_length = 12
    if len(streams) == 0:
        muses = list_muses()
        raise RuntimeError('Can\'t find EEG stream.')

    print("Collecting EEG data...")
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
    print('Sampling frequency: {}'.format(fs))


    """ Classify the state every 5 seconds """
    duration = 5
    # print('Start recording at time t=%.3f' % t_init)
    # print('Time correction: ', time_correction)
    
    # model = tf.keras.models.load_model(os.getcwd() + '/saved_models/both-gru_1024_dense_64_200.h5')
    model = tf.keras.models.load_model(os.getcwd() + '/saved_models/final-gru_1024_dense_256_200.h5')
    # while (time() - t_init) < duration:
    try:
        # 8/30: keep the last 2 confid_states from the previous 5 second interval
        last_twos = []

        while True:
            eeg_samples = []
            timestamps = []
            t_init = time()
            time_correction = inlet.time_correction()
            last_written_timestamp = None

            one_flag, two_flag, three_flag, four_flag = True, True, True, True

            while (time() - t_init) < duration:
                if (time() - t_init > 1 and time() - t_init < 1.1 and one_flag):
                    print(int(time() - t_init), end=' ')
                    one_flag = False
                elif (time() - t_init > 2 and time() - t_init < 2.1 and two_flag):
                    print(int(time() - t_init), end=' ')
                    two_flag = False
                elif (time() - t_init > 3 and time() - t_init < 3.1 and three_flag):
                    print(int(time() - t_init), end=' ')
                    three_flag = False
                elif (time() - t_init > 4 and time() - t_init < 4.1 and four_flag):
                    print(int(time() - t_init), end=' ')
                    four_flag = False
                
                try:

                    data, timestamp = inlet.pull_chunk(
                        timeout=1.0, max_samples=chunk_length)

                    if timestamp:
                        eeg_samples.append(data)
                        timestamps.extend(timestamp)
                        tr = time()
                    
                except KeyboardInterrupt:
                    break
                
            print('5, Generating matrix now..')

            eeg_samples = np.concatenate(eeg_samples, axis=0)
            timestamps = np.array(timestamps) + time_correction

            eeg_samples = np.c_[timestamps, eeg_samples]
            data = pd.DataFrame(data=eeg_samples, columns=["timestamps"] + ch_names)
            np_data = np.array(data)
            matrix = gen_training_matrix(np_data, [])

            """ 2. Make the raw prediction """
            raw_pred = model.predict(matrix)
            # print('raw_pred{}: '.format(raw_pred.shape))
            # print(raw_pred)

            """ 
            1. Determine the confidence of prediction 
            2. Determine if that confidence is continuing
            3. Actual state 1 & 2 matches
            """
            # i_pred = int(np.argmax(raw_pred))
            # print('i_pred: '.format(i_pred))
            
            # conf = raw_pred[i_pred]
            # print('conf: {}'.format(conf))


            """ 2. Interpret into readable result """
            pred_arr = np.array(list(map(lambda x: np.argmax(x), raw_pred)))

            print('pred_arr{}: {}'.format(pred_arr.shape, pred_arr))
            confids = []
            for i in range(raw_pred.shape[0]):
                confids.append(raw_pred[i][pred_arr[i]])

            confids = np.array(confids)
            print('confids{}: {}'.format(confids.shape, confids))
            
            
            confid_states = []
            # keep the last 2 confid_states from the previous 5 second interval
            for states in last_twos:
                confid_states.append(states)
            last_twos = []

            for i in range(len(confids)):
                if confids[i] >= 0.9:
                    confid_states.append(pred_arr[i])
                    
            # keep updating the last two states from the previous interval
            if len(confid_states) >= 2:
                last_twos.append(confid_states[-2:-1][0])
                last_twos.append(confid_states[-1:][0])

            confid_states = np.array(confid_states, dtype=object)
            print('last_twos: {}'.format(last_twos))
            print('confid_states{}: {}'.format(confid_states.shape, confid_states))

            # confid_states = np.array(confid_states)
            # counts = np.bincount(confid_states)
            # state_num = np.argmax(counts)
            # print('counts: {}'.format(counts))
            # counts = np.bincount(pred_arr)
            # state_num = np.argmax(counts)

            state_num = 4
            # check if a state is repeating 5 times consecutively
            for i in range(len(confid_states)-4):
                if confid_states[i] == confid_states[i+1] and confid_states[i] == confid_states[i+2]:
                    state_num = confid_states[i]

            if state_num == 2:
                print('Current state: Building')
                # commands.building()
            elif state_num == 1:
                print('Current state: Mining')
                # commands.mining()
            elif state_num == 0:
                print('Current state: Wandering')
                # commands.wandering()
            else:
                print('Not able to determine current state.')

            dur = 1000  # milliseconds
            freq = 440  # Hz

            # winsound.Beep(freq, dur)

    except KeyboardInterrupt:
        pass


    

    
