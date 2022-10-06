from __future__ import print_function
from __future__ import division
from builtins import str
from builtins import range
from past.utils import old_div
from PIL import Image
from PIL import ImageMath
from scipy import ndimage
import scipy
import numpy as np
import re
import os
import skimage.io as skio

#Updated as of 02/20/2020, by Bryan McCarty
#Updated for compatability with Python v3, scipy > v1.2

def exitProgram(msg):
    print(msg)
    exit(0)

def flatFieldingOneImage(inputStruct, inputDir, outputDir, NumFrames):
    Channels = inputStruct['channels']
    startFlatfieldPos = int(inputStruct['startFlatfieldPos']) 
    endFlatfieldPos = int(inputStruct['endFlatfieldPos']) 

    FFImages = {}
    Imgstr = str('%09d' %(0))
    for b in range (0, len(Channels)): #for each channel
        FF = []
        for a in range(startFlatfieldPos, endFlatfieldPos + 1): #for each Flatfield position
            try:
                img = skio.imread(os.path.join(inputStruct['inputParentPath'],inputStruct['prefix']+str(a),'img_'+Imgstr+'_'+Channels[b]+'_000.png')) # open image
                FF.append(np.array(img).astype(float)) #generates a stack of images.
            except:
                exitProgram('Cannot read images for flatFielding at '+ os.path.join(inputDir,'Img_'+Imgstr+'_'+Channels[b]+'_000.png'))
        FF= np.array(FF)

        FFImages[b] = ndimage.uniform_filter(np.median(FF, axis =0), size=5, mode="nearest") #calculates the median image smoothed
        FFImages[b]=old_div(np.double(FFImages[b]),np.max(np.max(FFImages[b], axis = 0), axis = 0)) # Normalizes FFimage

    #main loop
    for ii in NumFrames: # for each frame in 0th Channel ??? consider the frames of zero channel
        Imgstr = str('%09d' %(ii)) #creates the img number as a str of 9 digits with leading zeros
       
        for jj in range(0, len(Channels)): #for each channel **make it ||
            try:
                Img = np.double(skio.imread(os.path.join(inputDir,'Img_'+Imgstr+'_'+Channels[jj]+'_000.png'))) # open image
                FFImg = old_div(Img, FFImages[jj]) #Flatfield image
                FFImg = np.round(FFImg).astype(int)
#                scipy.misc.toimage(FFImg, mode = 'I', high = np.max(FFImg), low = np.min(FFImg)).save(path)
                skio.imsave(os.path.join(outputDir,'img_'+Imgstr+'_'+Channels[jj]+'_000.png'),np.uint16(FFImg),check_contrast=False)
            except:
                exitProgram('Cannot read/write images for flatFielding')

def flatFielding(inputStruct, inputDir, outputDir, NumFrames):
    Channels = inputStruct['channels']
    startFlatfieldPos = int(inputStruct['startFlatfieldPos']) 
    endFlatfieldPos = int(inputStruct['endFlatfieldPos']) 


    #main loop
    for ii in NumFrames: # for each frame in 0th Channel ??? consider the frames of zero channel
        Imgstr = str('%09d' %(ii)) #creates the img number as a str of 9 digits with leading zeros

        FFImages = {}
        for b in range (0, len(Channels)): #for each channel
            FF = []
            for a in range(startFlatfieldPos, endFlatfieldPos + 1): #for each Flatfield position
                try:
                    img = skio.imread(os.path.join(inputStruct['inputParentPath'],inputStruct['prefix']+str(a),'Img_'+Imgstr+'_'+Channels[b]+'_000.png')) # open image
                    FF.append(np.array(img).astype(float)) #generates a stack of images.
                    #print(type(img),type(Imgstr),type(FFImages),type(FF),type(Channels))
                except:
                    exitProgram('Cannot read images for flatFielding at '+ os.path.join(inputDir,'Img_'+Imgstr+'_'+Channels[b]+'_000.png'))
            FF= np.array(FF)

            FFImages[b] = ndimage.uniform_filter(np.median(FF, axis =0), size=5, mode="nearest") #calculates the median image smoothed
            FFImages[b]=old_div(np.double(FFImages[b]),np.max(np.max(FFImages[b], axis = 0), axis = 0)) # Normalizes FFimage
       
        for jj in range(0, len(Channels)): #for each channel **make it ||
            try:
                Img = np.double(skio.imread(os.path.join(inputDir,'Img_'+Imgstr+'_'+Channels[jj]+'_000.png'))) # open image
                FFImg = old_div(Img, FFImages[jj]) #Flatfield image
                FFImg = np.round(FFImg).astype(int)
#                scipy.misc.toimage(FFImg, mode = 'I', high = np.max(FFImg), low = np.min(FFImg)).save(path)
#                ImageMath.eval("convert(a,'I')",a = Image.fromarray(FFImg,mode ='I')).save(path)
                
                skio.imsave(os.path.join(outputDir,'img_'+Imgstr+'_'+Channels[jj]+'_000.png'),np.uint16(FFImg),check_contrast=False)
            except:
                exitProgram('Cannot read/write images for flatFielding')

