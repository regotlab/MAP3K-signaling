from __future__ import print_function
from __future__ import division
from builtins import str
from builtins import range
from past.utils import old_div
from PIL import Image
from PIL import ImageMath
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from scipy import ndimage
import tensorflow.keras.backend as K
import scipy
import numpy as np
import skimage.io
import skimage              
import skimage.morphology as skm
from skimage.util import *
import re
import os
import os.path
#import keras
import tensorflow as tf
from pathlib import Path
from .model_builder import *
from .metrics import *
from math import ceil
import psutil
import cv2 as cv
from natsort import natsorted
import natsort as ns

#generate batch lists
def batchgen(imlist,nbatch):
    for i in range(0,len(imlist),nbatch):
        yield imlist[i:i+nbatch]

#use Neural Net model
def useNNFull(inputStruct):
    
    tf.compat.v1.disable_v2_behavior()
    #configuring keras,tensorflow
    if inputStruct['useGPU']:
        configuration = tf.compat.v1.ConfigProto()
        #configuration.gpu_options.allow_growth = True
        #configuration.gpu_options.visible_device_list = "1"
        #configuration.gpu_options.per_process_gpu_memory_fraction = 0.8
        print('yay GPU')
    else:
        # Use the following configuration if you want to test on CPUs
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
        print('CPUs? Why?')
        configuration = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=1,inter_op_parallelism_threads=1)
    
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    run_opts = tf.compat.v1.RunOptions(report_tensor_allocations_upon_oom = True)
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
     
    session = tf.compat.v1.Session(config = configuration)
    tf.compat.v1.keras.backend.set_session(session)
    
    #determine which channel to use for segmentation
    nuclearChannel = inputStruct['nuclearMarkerChannel']
    
    #determine input folder
    if inputStruct['applyFlatFielding']:
        print('here')
        imageDir = inputStruct['outputParentPath']
    else:
        print('no here')
        imageDir = inputStruct['inputParentPath']
    print(imageDir)
    if len(inputStruct['processFrames']) == 0:
       kfs = 'allFrames'
    elif all(x >= 0 for x in inputStruct['processFrames']):
       kfs = 'posFrames'
       fr = inputStruct['processFrames']
       frlist = [str(f).zfill(9) for f in fr]
    elif all(x < 0 for x in inputStruct['processFrames']):
       kfs = 'negFrames'
       fr = [-x for x in inputStruct['processFrames']]
       frlist = [str(f).zfill(9) for f in fr]
    #imageDir = inputStruct['outputParentPath']
    
    image_list_prev = natsorted(Path(imageDir).rglob('*'+nuclearChannel+'*'), alg=ns.PATH)
    print(imageDir)
    print(nuclearChannel)
    #print(image_list_prev)

    if kfs == 'allFrames':    
        image_list = image_list_prev
    elif kfs == 'posFrames':
        image_list = [f for f in image_list_prev if f.stem[4:13] in frlist]
    elif kfs == 'negFrames':
        image_list = [f for f in image_list_prev if f.stem[4:13] not in frlist]
    
    #print("83")
    #print(image_list)
    
    #generate list of files in folder with correct channel marker in name
    image_names = [str(image_list[i]) for i in range(len(image_list))]
   # print("88")
    #print(image_names)
        
    if inputStruct['quite'] == False: print('Starting Neural Net Segmentation for ' + str(len(image_list)) + ' images')
    
    #calculates reasonable buffer size, max at 25% of RAM
    
    imnum = len(image_names) #total number of images
    tRAM = psutil.virtual_memory().total #total RAM on machine
    #print(imnum)
    #print(tRAM)
    
    if imnum > 10:   #determine size of single image to calc batch sizes
        imtestbuff = skimage.io.imread_collection(image_names[0:10])
        imtest = imtestbuff.concatenate()
        imtestsize = imtest.nbytes
        imtests1 = imtestsize/10
        imbuffsize = int(0.05*(tRAM/imtests1)) #max uses 5% total RAM per batch. Roughly 1500 1024x1024 16-bit for 64 GB ram.
        #print(imbuffsize)
    else:
        imtest = skimage.io.imread_collection(image_names[0]).concatenate()
        imbuffsize = imnum #max number of images at once
    
    #imbuffsize = 7 ##manually set number of images to process in each batch if for some reason the RAM code didn't work.
    
    dim1 = imtest.shape[1]
    dim2 = imtest.shape[2]
        
    batchNum = ceil(imnum/imbuffsize) #finds number of batches
    bGen = batchgen(image_names,imbuffsize)
    
    #load keras model

    #model = model_builder.get_model_3_class(dim1, dim2)
    
    model = get_model_3_class(dim1, dim2)
    model.load_weights(inputStruct['neuralNetModelPath'] )

    if inputStruct['quite'] == False: print('Neural net model loaded successfully.')    
    #if inputStruct['quite'] == False: model.summary()    
    
    k1 = skm.disk(1)
    k2 = skm.disk(2)
    k3 = skm.disk(3)   
    k4 = skm.disk(4)
    
    
    for j in range(0,batchNum):
        tf.compat.v1.keras.backend.clear_session()
        model = get_model_3_class(dim1, dim2)
        model.load_weights(inputStruct['neuralNetModelPath'] )

        #image_names_batched = [list1[i:i + 3] for i in range(0,len(list1),3)]    #create batched list
        if inputStruct['quite'] == False: print('Segmenting batch %s of %d.' % (j+1, batchNum))
        image_names_b = next(bGen) #generate batch list
        #print("143")
        #print(image_names_b)
        #print('listcreated')

        #load images
        imagebuffer = skimage.io.imread_collection(image_names_b)
        #print('imagesloaded')
        images = imagebuffer.concatenate()
        #print('concat')
        
        dim1 = images.shape[1]
        dim2 = images.shape[2]

        images = images.reshape((-1, dim1, dim2, 1))
        #print('reorg')

        # preprocess (assuming images are encoded as 16-bits in the preprocessing step)
        images = images / 255
        #print('div')

        #run predictions
        predictions = model.predict(images, batch_size=1)
        print('predict')
        #if inputStruct['quite'] == False: print('Neural Net predictions successful. Saving NN predictions.')
        
        if inputStruct['cell_min_size'] == 0: #sets minimum nucleus size in pixels
            cellmin = 16
            #cellmin = 4
        else:
            cellmin = inputStruct['cell_min_size']
            
          #transform to label matrices, save images

        for i in range(len(images)):
            fname = image_list[i + imbuffsize*j]
            bname = os.path.join(str(fname.parent),fname.stem[0:14])
            
            probmap = predictions[i].squeeze()
            
            pred = probmap_to_pred(probmap,2)
            
            label = pred_to_label(pred,cellmin)
            label = img_as_ubyte(np.divide(label,np.max(label)))
            #label = cv.erode(label,k1)
            l1 = label
            l2 = label
            l3 = label
            label = cv.morphologyEx(label,cv.MORPH_OPEN,k2) 
            [label, num] = skimage.morphology.label(label, return_num=True)
            label = skimage.morphology.remove_small_objects(label, min_size=cellmin,connectivity=1)
            label = img_as_ubyte(np.divide(label,np.max(label)))


            
            if inputStruct['saveNNProbMap']:
                skimage.io.imsave(bname + 'NNprob_000.png', img_as_ubyte(np.divide(probmap,np.max(probmap))),check_contrast=False) #img_as_ubyte converts img type to 255 before save
                skimage.io.imsave(bname + 'NNpred_000.png', img_as_ubyte(np.divide(pred,np.max(pred))),check_contrast=False)

            skimage.io.imsave(bname + 'NNseg_000.png', label,check_contrast=False)

            
        
        images = None
        predictions = None
