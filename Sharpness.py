# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 16:05:58 2022

@author: birib
"""

def Sharpness (path_in,path_out):
  
  os.mkdir(path_out)
  
  ##### Trasformation Loop ####
    
  directory = os.fsencode(path)

  for file in os.listdir(directory):
    filename = os.fsdecode(file)
    image = img.imread(path+filename)

  # ----- TRASFORMAZIONE ------
 
    transformed = transform(image=image)
    transformed_image = transformed["image"]

  # ---------------------------

    img.imsave(path_out+'/'+filename,transformed_image)
    k = k+1  
  #############################
    
  print(str(k)+'images of the current class have been saved')