# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 22:26:58 2022

@author: Antonio Vispi
"""

import argparse
import os
import numpy as np
import skimage.io as img


def extrapolate_parameters(input_percentages,input_classes):
  c = '#'
  support = [pos for pos, char in enumerate(input_percentages) if char == c]
  percentages = np.zeros(len(support)-1)
  for i in range (0,len(support)-1):
    percentages[i] = (input_percentages[(support[i]+1):(support[i+1])])
  support = [pos for pos, char in enumerate(input_classes) if char == c]
  classes = []
  for i in range (0,len(support)-1):
    classes.append(input_classes[(support[i]+1):(support[i+1])])
  if len(classes)!=len(percentages):
    print('Error! Double-check that the percentage vector and the class vector are in the recommended format.')
    classes = []
    percentages = []
  return percentages , classes


def counter(directory):
  k=0
  for file in os.listdir(directory):
    filename = os.fsdecode(file)
    k=k+1
  return k

print('Image splitting is 70% for the training set, 20% for the test set, and 10% for the validation set.')
print('\n')



def make_dataset(path_in,path_out,percentages_in,classes_in,classes_out):

    percentages , classes = extrapolate_parameters(percentages_in,classes_in)
    percentages , classes_output = extrapolate_parameters(percentages_in,classes_out)


    if len(classes_output) != len(classes):
      print('Mistake! Double check that the names of the input and output classes are in the right order and in equal number')
    
    os.makedirs(path_out, exist_ok = True)
    os.makedirs(path_out+'/test_set/test_set', exist_ok = True)
    os.makedirs(path_out+'/training_set/training_set', exist_ok = True)
    os.makedirs(path_out+'/val_set/val_set', exist_ok = True)
    for i in range(len(classes)):
      os.makedirs(path_out+'/test_set/test_set/'+classes_output[i], exist_ok = True)
      os.makedirs(path_out+'/training_set/training_set/'+classes_output[i], exist_ok = True)
      os.makedirs(path_out+'/val_set/val_set/'+classes_output[i], exist_ok = True)
    
      
    # Specify the file name
    file = 'classes.txt'
    
    # Creating a file at specified location
    with open(os.path.join(path_out, file), 'w') as fp:
        pass
        # To write data to new file uncomment
        string=''
        for i in range(0,len(classes)):string = string+classes_output[i]+'\n'
        fp.write(string)
      
    # After creating 
    print("File .txt just created:")
    print('\n')
    print(string)
    
    
    for i in range (len(classes)):
    
        Counter_test = 0 # Count of total training images saved by class
        Counter_train = 0 # Count of total training images saved by class
        Counter_val = 0 # Count of total training images saved by class
    
        directory = os.fsencode(path_in+'/'+classes[i])
        images_num = counter(directory)
    
        quotaparte_20 = round(((images_num*percentages[i])/100)*20);
        quotaparte_90 = round((images_num*percentages[i]/100)*90);
        randomized_indices = np.random.permutation(images_num)
        all_images = os.listdir(path_in+'/'+classes[i])
        
        # TEST SET
        for m in range(0,quotaparte_20 +1):
          name = all_images[randomized_indices[m]]
          image = img.imread(path_in+'/'+classes[i]+'/'+name)
          img.imsave(path_out+'/test_set/test_set/'+classes_output[i]+'/'+name,image)
          Counter_test = Counter_test + 1 
        print('A total of '+str(Counter_test)+' images of the '+classes_output[i]+' class were saved in the test set...')
        # TRAINING SET
        for m in range(quotaparte_20 +1,quotaparte_90 +1):
          name = all_images[randomized_indices[m]]
          image = img.imread(path_in+'/'+classes[i]+'/'+name)
          img.imsave(path_out+'/training_set/training_set/'+classes_output[i]+'/'+name,image)
          Counter_train = Counter_train + 1 
        print('A total of '+str(Counter_train)+' images of the '+classes_output[i]+' class were saved in the training set...') 
        # VALIDATION SET
        for m in range(quotaparte_90 + 1, round(images_num*percentages[i])):
          name = all_images[randomized_indices[m]]
          image = img.imread(path_in+'/'+classes[i]+'/'+name)
          img.imsave(path_out+'/val_set/val_set/'+classes_output[i]+'/'+name,image)
          Counter_val = Counter_val + 1 
        print('A total of '+str(Counter_val)+' images of the '+classes_output[i]+' class were saved in the validation set...')  
        
        print('A total of '+str(Counter_test+Counter_train+Counter_val)+' images of the '+classes_output[i]+' class were saved.')
        print('\n')
    
    print('The dataset was successfully defined or updated.')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_in', help='input path of the directory containing all classes')
    parser.add_argument('--path_out', help='output path for saving the entire dataset')
    parser.add_argument('--percentages_in', help='Ordered percentages of each single class [0,1], where 1 means 100%, of the images to be taken from the input dataset.')
    parser.add_argument('--classes_in', help='Ordered names of all classes belonging to path_in')
    parser.add_argument('--classes_out', help='Ordered names of all classes belonging to the output destination path (path_out).')

    args = parser.parse_args()
    make_dataset(args.path_in,args.path_out,args.percentages_in,args.classes_in,args.classes_out)
    
if __name__ == '__main__':
    main()

