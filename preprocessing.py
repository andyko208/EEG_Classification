import numpy as np
import pandas as pd
import os


def get_dataset():
    directory = os.getcwd() + '/eeg-feature-generation/dataset/original_data/'
    for filename in os.listdir(directory):
        df = pd.read_csv(directory + filename)
        
