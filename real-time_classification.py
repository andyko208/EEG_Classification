import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import os
import random

from sklearn.model_selection import train_test_split

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
