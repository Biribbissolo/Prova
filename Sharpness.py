# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 16:05:58 2022

@author: Antonio Vispi
"""
import argparse
import albumentations as A
import skimage.io
import matplotlib.pyplot as plt
import skimage.io as img
import cv2
import os
import random


# Dichiarazione della augmentation pipeline : Sharpen Delicata 

transform = A.Compose([
          A.Sharpen (alpha=(0.2, 0.2), lightness=(1, 1), always_apply=True, p=1),  #Trasformazione di leggero Sharpness che altera poco la luminosità
])

def Sharpness (path_in,path_out):

  print('Your class is processing...')
  
  os.mkdir(path_out, exist_ok = True)
  
  ##### Trasformation Loop ####
    
  directory = os.fsencode(path_in)

  k=0

  for file in os.listdir(directory):
    filename = os.fsdecode(file)
    image = img.imread(path_in+'/'+filename)

    # ----- TRASFORMAZIONE ------
 
    transformed = transform(image=image)
    transformed_image = transformed["image"]

    # ---------------------------

    img.imsave(path_out+'/'+filename,transformed_image)
    k = k+1  
    #############################
    
  print(str(k)+' images of the current class have been saved')
  print('Now you can move on to the next class')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_in', help='input path of the specific class')
    parser.add_argument('--path_out', help='output path for saving the specific class')

    args = parser.parse_args()
    Sharpness (args.path_in,args.path_out)

if __name__ == '__main__':
    main()
