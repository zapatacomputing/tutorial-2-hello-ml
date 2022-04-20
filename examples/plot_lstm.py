################################################################################
# © Copyright 2020 Zapata Computing Inc.
################################################################################
"""
Copyright Zapata Computing, Inc. All rights reserved.

Plot the loss function values and predictions from the results of the
`lstm-tutorial.yaml` workflow.
"""

import sys
import json
import pandas as pd
from matplotlib import pyplot as plt

def plot(filename):
    # Insert the path to your JSON file here
    try:
        with open(filename) as f:
            results = json.load(f)
    except IOError:
        print(f'Error: {filename} not found.')

    training_loss_vals = []
    validation_loss_vals = []
    predicted_vals = []

    for step in results:
        if results[step]['class'] == 'train-model':
            training_loss_vals = results[step]['history']['history']['loss']
            validation_loss_vals = results[step]['history']['history']['val_loss']
        if results[step]['class'] == 'preprocess-data':
            training_df = pd.DataFrame(results[step]['training-data']['data'])
            testing_df = pd.DataFrame(results[step]['testing-data']['data'])
        if results[step]['class'] == 'predict-using-model':
            predicted_vals_obj = results[step]['predictions']['data']
            for entry in predicted_vals_obj:
                predicted_vals.append(entry['data'][0]['data'])

    # Converting indices to ints and sorting by indices
    training_df.index = training_df.index.astype(int)
    training_df.sort_index(inplace=True)
    testing_df.index = testing_df.index.astype(int)
    testing_df.sort_index(inplace=True)

    # Plotting values from training process
    plt.figure()
    plt.plot(training_loss_vals, label='Train')
    plt.plot(validation_loss_vals, label='Validation')
    plt.xlim(left=0.0)
    plt.ylim(bottom=0.0)
    plt.grid()
    plt.legend()
    plt.title("Loss function: MSE")
    plt.xlabel('Epoch')
    plt.ylabel('Loss function value')

    # Plotting results: train, test and perdicted datasets
    plt.figure()

    plt.plot(training_df['time'], training_df['values'], color='g', label="Training", zorder=2)
    plt.plot(testing_df['time'], testing_df['values'], color='b', label="Testing", zorder=3)
    plt.scatter(testing_df['time'].values[10:], predicted_vals, marker='o', s=15., color='r', label="Predicted", zorder=4)

    plt.ylabel('Value')
    plt.xlabel('Time')
    plt.legend()
    plt.grid()
    plt.title("Training, Test and Predicted datasets")

    plt.show()


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        print(f'Error: please pass the JSON result file to be plotted.')
        sys.exit(1)

    plot(filename)
