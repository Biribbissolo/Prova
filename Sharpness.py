# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 16:05:58 2022

@author: birib
"""

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
  
  os.mkdir(path_out)
  
  ##### Trasformation Loop ####
    
  directory = os.fsencode(path_in)

  for file in os.listdir(directory):
    filename = os.fsdecode(file)
    image = img.imread(path_in+filename)

  # ----- TRASFORMAZIONE ------
 
    transformed = transform(image=image)
    transformed_image = transformed["image"]

  # ---------------------------

    img.imsave(path_out+'/'+filename,transformed_image)
    k = k+1  
  #############################
    
  print(str(k)+'images of the current class have been saved')