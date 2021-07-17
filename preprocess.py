import os
import pandas as pd
import numpy as np

# 1. Reformat the timestamp (÷ 1,000,000) that period of 1.0 can actually represent 1 second in the timestamp of the dataset (currently 1,000,000 represents one second period)
# 2. Export the new dataset into my_new_data
# 3. Perform feature extraction over my_new_data folder

def reformat_timestamp_n_export(raw_dir, new_dir):
    
    # ~/new_dataset
    if not os.getcwd() + '/new_dataset':
        os.mkdir('/new_dataset')
        
    # ~/new_dataset/filename        
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    
    files = os.listdir(raw_dir)
    for file in files:
        if '.csv' in file:
            print(file)
            df = pd.read_csv(raw_dir + '/' + file)
            for i in range(df['timestamps'].shape[0]):
                timestamp = df['timestamps'][i]/1000000.0
                df['timestamps'][i] = timestamp
            df.to_csv(new_dir + '/' + file, index=False)
            
def new_dataset(filename):
    
    raw_dir = os.getcwd() + '/raw_dataset/' + filename
    new_dir = os.getcwd() + '/new_dataset/' + filename
    print('Writing the outfile to \'{}\''.format(new_dir))
    
    reformat_timestamp_n_export(raw_dir, new_dir)
    
# Edit filename (from raw dataset folder) here
# filename = 'my-mental-state'

# new_dataset(filename)