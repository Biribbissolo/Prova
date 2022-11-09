# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 17:03:26 2022

@author: birib
"""

import argparse
import json
import matplotlib.pyplot as plt
import numpy as np


def load_json_arr(json_path):
    lines = []
    with open(json_path, 'r') as f:
        for line in f:
            lines.append(json.loads(line))
    return lines

def training_graphs(path_in_json):

  experiment_metrics = load_json_arr(path_in_json)

  Val_Losses=[]
  Train_Losses=[]
  for sample in experiment_metrics[1:len(experiment_metrics)]:
    if sample['mode'] == 'val':
      if 'loss' in sample:
        Val_Losses.append(sample['loss'])
    if sample['mode'] == 'train':
      if 'loss' in sample:
        Train_Losses.append(sample['loss'])

  Val_Accuracy=[]
  Train_Accuracy=[]
  for sample in experiment_metrics[1:len(experiment_metrics)]:
    if sample['mode'] == 'val':
      if 'accuracy_top-1' in sample:
        Val_Accuracy.append(sample['accuracy_top-1'])
    if sample['mode'] == 'train':
      if 'top-1' in sample:
        Train_Accuracy.append(sample['top-1'])

  Epoch_Train = np.linspace(1, 160, num=800)
  Epoch_Val = np.linspace(1, 160, num=160)

  fig, axs = plt.subplots(1,2, figsize=(20, 15))
  plt.rcParams['font.size'] = 18

  plt.sca(axs[0])
  plt.yticks(np.arange(0, max(max(Val_Losses),max(Train_Losses)), 0.1))
  axs[0].plot(Epoch_Val,Val_Losses,Epoch_Train,Train_Losses)
  axs[0].set_title('Model Losses')
  axs[0].set(xlabel='Epoch')
  axs[0].set(ylabel='Loss')
  axs[0].legend(('Validation', 'Training'), loc='upper right', shadow=True)

  plt.sca(axs[1])
  plt.yticks(np.arange(0, max(max(Val_Accuracy),max(Train_Accuracy)), 5))
  axs[1].plot(Epoch_Val,Val_Accuracy,Epoch_Train,Train_Accuracy)
  axs[1].set_title('Model Accuracy')
  axs[1].set(xlabel='Epoch')
  axs[1].set(ylabel='Accuracy(%)')
  axs[1].legend(('Validation', 'Training'), loc='lower right', shadow=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_in_json', help='Enter the path of the .json file containing all the annotations of the model training data')

    args = parser.parse_args()
    training_graphs(args.path_in_json)

if __name__ == '__main__':
    main()