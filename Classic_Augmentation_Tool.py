# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 15:03:16 2022

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

def Classic_Augmentation (path_in, path_out, Telescope_multiplicator, Super_Telescope_multiplicator, Rectangle_multiplicator):

    path_C = (path_in+'/telescope/')                # Telescope
    path_SC = (path_in+'/super_Telescope/')         # Super_Telescope
    path_R = (path_in+'/rectangle/')                  # Rectangle 
    
    destinazione = (path_out+'/')       # FINAL PATH
    os.mkdir(path_out)
    
    
    ##################################################################################################################################################################################
    
                                                 ######################################################################
                                                 #                                                                    #
                                                 #    We start from photos with circular black artifact: telescope    #
                                                 #                                                                    #
                                                 ######################################################################
    
    ##################################################################################################################################################################################                                             
    
    
    
    
    
    label= ('C_')
    
    # To give strength, you must avoid that similar photos are saved in groups,
    # therefore we define a random 4-digit pin to be placed at the beginning of the name of all the photos, in order to mix them when saving
    
    directory = os.fsencode(path_C)
    counter = 0         
    Counter_TOT = 0                      # Counter of all saved photos
    
    for file in os.listdir(directory):
         filename = os.fsdecode(file)
         image = img.imread(path_C+filename)
    # ---------------------------------- INITIAL TRANSFORMATION --------------------
    
         # Declare transformation : 1° Trasformazione : Rotate + Crop
         transform = A.Compose([
                  A.Rotate (limit=[45, 45], interpolation=1, border_mode=0, value=None, mask_value=None, rotate_method='largest_box', crop_border=True, always_apply=True, p=1),
         ]) 
    
         transformed = transform(image=image)
         image = transformed["image"]
         #  --- ADD ---
         dimension= image.shape
         height = round((dimension[0]/100)*86)  # new height : 86%
         width = round((dimension[1]/100)*86)   # new width : 86%
         #  -----------
    
    # -------------------------------------------------------------------------------
    
          
         for i in range (1,Telescope_multiplicator):  # Photos have increased by a factor of 'Telescope_multiplicator'
           
           if i==1:
             transform = A.Compose([                                        
                      A.CenterCrop (height, width, always_apply=True, p=1), 
             ])                                                             
             transformed = transform(image=image)                           
             transformed_image = transformed["image"]                       
    
             Pin = str(random.randint(1, 9999))+'_'
             img.imsave((destinazione+Pin+label+'1_'+filename),transformed_image) # Save the first rotated + crop image only  
             counter = counter + 1
    
           else:
             # Declare transformation: 2nd Transformation. Various augmentation.
             transform = A.Compose([
                      A.PiecewiseAffine (scale=(0.025, 0.045), nb_rows=4, nb_cols=4, interpolation=5, mask_interpolation=0, cval=0, cval_mask=0, mode='constant', absolute_scale=False, always_apply=True, keypoints_threshold=0.01, p=1),
                      A.Flip(always_apply= False, p=0.5),
                      A.Transpose(always_apply= False, p=0.5),
                      A.RandomRotate90(always_apply= False, p=0.5),
                      A.CenterCrop (height, width, always_apply=True, p=1), 
             ]) 
    
             transformed = transform(image=image)
             transformed_image = transformed["image"]
    
             Pin = str(random.randint(1, 9999))+'_'
             img.imsave(destinazione+Pin+label+str(i)+'_'+filename,transformed_image) # Except subsequent images submitted to Albumentation 
             counter = counter + 1
    
    print('They were saved '+str(counter)+' images successfully from Telescope images.')
    Counter_TOT = Counter_TOT + counter
    #################################################################################################################################################################################
    
                                                      ##################################################################################
                                                      #                                                                                #
                                                      #   It starts with photos with VERY circular black artifact:  Super_Telescope    #
                                                      #                                                                                #
                                                      ##################################################################################
    
    #################################################################################################################################################################################
    
    label= ('SC_')
    
    directory = os.fsencode(path_SC)
    counter = 0
    
    for file in os.listdir(directory):
         filename = os.fsdecode(file)
         image = img.imread(path_SC+filename)
    
         # ---------------------------------- INITIAL TRANSFORMATION -----------------
         # Declare an augmentation pipeline: 1st Transformation: Rotate + Crop
         transform = A.Compose([
                  A.Rotate (limit=[45, 45], interpolation=1, border_mode=0, value=None, mask_value=None, rotate_method='largest_box', crop_border=True, always_apply=True, p=1),
         ])  
         # Augment an image
         transformed = transform(image=image)
         image = transformed["image"]
    
         dimension= image.shape
         height = round((dimension[0]/100)*72)  # Nuova altezza : 72%
         width = round((dimension[1]/100)*72)   # Nuova larghezza : 72%
    
         # Declare an augmentation pipeline: 2°.  Transformation : Center Crop 72 %
         transform = A.Compose([
                  A.CenterCrop (height, width, always_apply=True, p=1), 
         ])  
    
         # Augment an image
         transformed = transform(image=image)
         image = transformed["image"]
    
         # ----------------------------------------------------------------------------
    
          
         for i in range (1,Super_Telescope_multiplicator):   # Photos have increased by a factor of 'Super_Telescope_multiplicator'
           
           if i==1:
             Pin = str(random.randint(1, 9999))+'_'
             img.imsave((destinazione+Pin+label+'1_'+filename),image) # Saving the first image rotated + crop + centerCrop only
             counter = counter + 1
           else:
              # Declare an augmentation pipeline 3rd Transformation: Various augmentation. Note: The following PiecewiseAffine is more delicate than the others in this block. 
              transform = A.Compose([
                      A.PiecewiseAffine (scale=(0.025, 0.045), nb_rows=3, nb_cols=3, interpolation=5, mask_interpolation=0, cval=0, cval_mask=0, mode='constant', absolute_scale=False, always_apply=True, keypoints_threshold=0.01, p=1),
                      A.Flip(always_apply= False, p=0.5),
                      A.Transpose(always_apply= False, p=0.5),
                      A.RandomRotate90(always_apply= False, p=0.5),
              ])  
    
              # Augment an image
              transformed = transform(image=image)
              transformed_image = transformed["image"]
    
              Pin = str(random.randint(1, 9999))+'_'
              img.imsave(destinazione+Pin+label+str(i)+'_'+filename,transformed_image) # Saving subsequent images subjected to Albumentation
              counter = counter + 1
    
    print('They were saved '+str(counter)+' images successfully from Super_Telescope images.')
    Counter_TOT = Counter_TOT + counter
    #################################################################################################################################################################################
    
                                                      ##################################################################################
                                                      #                                                                                #
                                                      #         We start with Rectangular or Square photos: Rectangle                  #
                                                      #                                                                                #
                                                      ##################################################################################
    
    #################################################################################################################################################################################
    
    
    directory = os.fsencode(path_R)
    counter = 0
    
    for file in os.listdir(directory):
         filename = os.fsdecode(file)
         image = img.imread(path_R+filename)
    
        ####### Controllo Aspect Ratio #######
         dimensions = image.shape
         dimensions = dimensions [0:2]                # I only care about height and width, not the number of channels.
         if dimensions[1] >= (dimensions[0] * 1.5):   # Control: is it really a rectangle?
           
           # --- Sliding Windows ---  
           image_L=image[0:min(dimensions),0:min(dimensions)]
           image_C=image[0:min(dimensions),round(max(dimensions)/2)-round(min(dimensions)/2):round(max(dimensions)/2)+round(min(dimensions)/2)]
           image_R=image[0:min(dimensions),max(dimensions)-min(dimensions):max(dimensions)]
           # -----------------------
    
           # Declare an augmentation pipeline : Albumentations vari
           transform = A.Compose([
                   A.PiecewiseAffine (scale=(0.025, 0.045), nb_rows=4, nb_cols=4, interpolation=5, mask_interpolation=0, cval=0, cval_mask=0, mode='constant', absolute_scale=False, always_apply=True, keypoints_threshold=0.01, p=1),
                   A.Flip(always_apply= False, p=0.5),
                   A.Transpose(always_apply= False, p=0.5),
                   A.RandomRotate90(always_apply= False, p=0.5),
           ])
    
           # --- Transformations + Saving ---
           transformed = transform(image=image_L)
           transformed_image = transformed["image"]
           Pin = str(random.randint(1, 9999))+'_'
           label= ('RL_')
           img.imsave((destinazione+Pin+label+filename),transformed_image)
           counter = counter + 1
          
           transformed = transform(image=image_C)
           transformed_image = transformed["image"]
           Pin = str(random.randint(1, 9999))+'_'
           label= ('RC_')
           img.imsave((destinazione+Pin+label+filename),transformed_image)
           counter = counter + 1
    
           transformed = transform(image=image_R)
           transformed_image = transformed["image"]
           Pin = str(random.randint(1, 9999))+'_'
           label= ('RR_')
           img.imsave((destinazione+Pin+label+filename),transformed_image)
           counter = counter + 1
           # -----------------------------------
    
         else:   # If, on the other hand, the image is not so rectangular ...
          
           for i in range (1,Rectangle_multiplicator):                  # Photos have increased by a factor of 'Rectangular_multiplicator'
    
             if i==1:
    
                # Declaration of an augmentation pipeline : Center Crop to make the image exactly square
               transform = A.Compose([
                         A.CenterCrop (min(dimensions), min(dimensions), always_apply=True, p=1), 
               ])  
               
               transformed = transform(image=image)
               transformed_image = transformed["image"]
    
               Pin = str(random.randint(1, 9999))+'_'
               label= ('Q_')
               img.imsave((destinazione+Pin+label+'1_'+filename),transformed_image)
               counter = counter + 1
             else:
               # Declaration of an augmentation pipeline : Various Albumentations (I perform the elastic twisting before the crop, because in this way the final result is better)
               transform = A.Compose([
                         A.PiecewiseAffine (scale=(0.025, 0.045), nb_rows=4, nb_cols=4, interpolation=5, mask_interpolation=0, cval=0, cval_mask=0, mode='constant', absolute_scale=False, always_apply=True, keypoints_threshold=0.01, p=1),
                         A.Flip(always_apply= False, p=0.5),
                         A.Transpose(always_apply= False, p=0.5),
                         A.RandomRotate90(always_apply= False, p=0.5),
               ])
               transformed = transform(image=image)
               transformed_image = transformed["image"]
    
               new_dimensions = transformed_image.shape
               new_dimensions = new_dimensions [0:2] 
               # Declaration of an augmentation pipeline : Center Crop to make the image exactly square
               transform = A.Compose([
                         A.CenterCrop (min(new_dimensions), min(new_dimensions), always_apply=True, p=1), 
               ])  
               
               transformed = transform(image=transformed_image)
               transformed_image = transformed["image"]
    
               Pin = str(random.randint(1, 9999))+'_'
               label= ('Q_')
               img.imsave(destinazione+Pin+label+str(i)+'_'+filename,transformed_image)
               counter = counter + 1
    
    print('They were saved '+str(counter)+' images successfully from Rectangle images.')
    Counter_TOT = Counter_TOT + counter
    print('A total of '+str(Counter_TOT)+' pictures of your class have been successfully saved! Please, go on with the next class.')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path_in', help='input path of the specific class')
    parser.add_argument('path_out', help='output path for saving the specific class')
    parser.add_argument('Telescope_multiplicator', help='Black Artifact Image Multiplication Factor (Telescope)')
    parser.add_argument('Super_Telescope_multiplicator', help='Multiplication factor of images with a lot of black artifact (Super_Telescope)')
    parser.add_argument('Rectangle_multiplicator', help='Image multiplication factor without black artifact (Rectangular)')

    args = parser.parse_args()
    Classic_Augmentation (args.path_in,args.path_out,args.Telescope_multiplicator,args.Super_Telescope_multiplicator,args.Rectangle_multiplicator)

if __name__ == '__main__':
    main()
