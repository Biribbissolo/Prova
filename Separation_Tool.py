# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 17:21:03 2022

If you need to change the thresholds of the separation test, 
in order to separate your images more correctly,
please change them in the Test Section (function : telescope_test).

@author: Antonio Vispi
"""



import argparse
import skimage.io as img
from skimage.color import rgb2gray
from skimage.transform import resize
import numpy as np
import os

def convert(img, target_type_min, target_type_max, target_type):
    imin = img.min()
    imax = img.max()

    a = (target_type_max - target_type_min) / (imax - imin)
    b = target_type_max - a * imax
    new_img = (a * img + b).astype(target_type)
    return new_img

def telescope_test(image):

  img = rgb2gray(image)
  img = resize(img, (512, 512))  # make all the images square
  img = convert(img, 0, 255, np.uint8)

  mask_1 = np.ones([512,512], dtype=np.uint8)
  mask_1[15:len(mask_1)-15,15:len(mask_1)-15] = 0  #mask consisting of the outer frame 15 pixels wide
  norm_1 = np.sum(mask_1) #number of non-zero pixels of the thin mask
  immagine_1 = img * mask_1;   # I just look at the picture frame, the rest is 0

  mask_2 = np.ones([512,512], dtype=np.uint8)
  mask_2[60:len(mask_2)-60,60:len(mask_2)-60] = 0 #mask consisting of the outer frame 60 pixels wide
  norm_2 = np.sum(mask_2);   #number of non-zero pixels of the thin mask
  immagine_2 = img * mask_2;   # I just look at the picture frame, the rest is 0


  ###########  Test Section  #########
  if np.sum(immagine_2)/norm_2 <= 2.5 and np.sum(immagine_1)/norm_1 < 103:
    Test = 2;           # there is a lot of black ----> Photos with a lot of black circular border

  elif np.sum(immagine_1)/norm_1 < 103:
    Test = 0;           # there is black ----> Photo with black circular border                    

  elif np.sum(immagine_1)/norm_1 >= 103:
    Test = 1;         # little black around ----> Full Rectangular Photo
  
  return Test
  ####################################

def Separator (path_in,path_out):
  print('Your class separation is processing...')
  print('\n')
  
  os.mkdir(path_out)
  os.mkdir(path_out+'/telescope/')
  os.mkdir(path_out+'/super_telescope')
  os.mkdir(path_out+'/rectangle')
  
  ##### Loop #####
    
  directory = os.fsencode(path_in)
  
  telescope = 0
  super_telescope = 0
  rectangle = 0
  

  for file in os.listdir(directory):
    filename = os.fsdecode(file)
    image = img.imread(path_in+'/'+filename)

    # ----- TEST ------
 
    Test = telescope_test(image) 

    # -----------------
    if Test == 1:                  # Image without black artifact
      img.imsave(path_out+'/rectangle/'+filename,image)
      rectangle = rectangle + 1 
    elif Test == 0:                # Image with black artifact
      img.imsave(path_out+'/telescope/'+filename,image)
      telescope = telescope + 1 
    elif Test == 2:                # Image with a lot of black artifact
      img.imsave(path_out+'/super_telescope/'+filename,image)
      super_telescope = super_telescope + 1  
  
  print(str(rectangle)+' images without black artifact (Rectangular images)\n'+str(telescope)+' with black artifact (Telescope images)\n'+str(super_telescope)+' with a lot of black artifact (Super-telescope images)\nwere saved.')
  print('\n')
  print('Now you can move on to the next class')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_in', help='input path of the specific class')
    parser.add_argument('--path_out', help='outpu path for saving the specific class')

    args = parser.parse_args()
    Separator (args.path_in,args.path_out)

if __name__ == '__main__':
    main()
