# EEG_Classification

![BCI_Steps](bci_steps.png)

## Current Stage
- Collected dataset that consist of raw signal values from muse headset in dataset/raw_dataset/
- Converted raw dataset to generate training data in dataset/training_dataset/ using EEG_feature_extraction.py & EEG_generate_training_matrix.py
- The models in saved_models/ are trained with different hyperparameters settings, and best cases are saved.
- However, these models all have a limitation in not being able to make accurate predictions when the signal values become stabilized.

## Future Goals
- Collect new dataset from directions in muse_setup
- Now the dataset will be stabilized, also with one more state added (Stationary state)
- Refer to current model hyperparameter settings and update model accordingly to be able to classify between 4 states (uncomment some code that I've made)
- Update real-time_classification.py file accordingly (uncomment some code that I've made) to also take the change of model in effect.
