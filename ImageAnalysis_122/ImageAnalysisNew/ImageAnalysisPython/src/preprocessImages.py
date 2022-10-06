'''


'''
from __future__ import print_function
from __future__ import absolute_import

from builtins import str
from builtins import range
import re
import os
import shutil
from .flatfielding import *
from .registerAndCrop import *
from .neuralSegmentFull import *
import json
from joblib import Parallel, delayed
from joblib.externals.loky import get_reusable_executor 
import multiprocessing
import copy


def exitMsg(msg):
    print(msg)
    exit()

def checkInputParam(inputStruct):

    #assign optional inputs
    # using fracAreaAlign of 0 is not recommended. it does no registration or cropping, but just pads with the median.
    # fracAreaAlign of 0 saves no time compared to using 0.5.
    inputStruct['fracAreaAlign'] = 0.5 

    # check validity of processFrames 
    if any(x >= 0 for x in inputStruct['processFrames']) and any(x < 0 for x in inputStruct['processFrames']): 
        exitMsg('processFrames cannot have both values >=0 and values <0.')

    #if len(inputStruct['channels']) != len(inputStruct['flatfieldingFuncs']) or (len(inputStruct['channels']) != len(inputStruct['flatfieldingVarargs'])):
    #    exitMsg('channels, flatfieldingFuncs, and flatfieldingVarargs must all be the same length.')
    if inputStruct['applyNeuralNetSegmentation']:
        nuclearChannel = inputStruct['nuclearMarkerChannel']
        if nuclearChannel not in inputStruct['channels']:
            exitMsg('The indicated channel for neural net segemntation' + inputStruct['nuclearMarkerChannel'] + 'is not in the channel list')

    if os.path.isdir(inputStruct['inputParentPath']) == False:
        exitMsg('The folder '+inputStruct['inputParentPath']+' does not exist')
    else:
        if os.path.isdir(inputStruct['outputParentPath']) == False:
            try: os.makedirs(inputStruct['outputParentPath'])
            except: exitMsg('Cannot create the output directory: '+inputStruct['outputParentPath'])

    num_cores = multiprocessing.cpu_count()
    if inputStruct['CPU_NUMs'] == 0 or inputStruct['CPU_NUMs'] > num_cores: inputStruct['CPU_NUMs'] = num_cores
 
    return inputStruct


def callPreprocessImagesSubfolder(inputStruct):
    # check existence of subfolders
    dirListPre = os.listdir(inputStruct['inputParentPath'])
    print('InputParent is' + inputStruct['inputParentPath'])
    dirListFull = []
    for i in dirListPre:
        fullPath = os.path.join(inputStruct['inputParentPath'], i)
        if (i.startswith('.') == False) and os.path.isdir(fullPath): dirListFull.append(i)
    if len(inputStruct['subfolderNames']) == 0: dirList = dirListFull
    else:
        dirList = []
        for i in inputStruct['subfolderNames']:
            if i in dirListFull: dirList.append(i)
            else: print('Warning: ',i, 'subfolder does not exist in ', inputStruct['inputParentPath'])


    if inputStruct['applyFlatFielding']:
        for a in range(inputStruct['startFlatfieldPos'], inputStruct['endFlatfieldPos'] + 1):
            name = inputStruct['prefix']+str(a)
            if name in dirList: dirList.remove(name)   
            
            
    ## this loop is parallel - flatfielding
    p1 = Parallel(n_jobs=inputStruct['CPU_NUMs'])
    results = p1((delayed(preprocessFFSubfolder)(inputStruct, subfolderNow) for subfolderNow in dirList))
    p1._aborted = True
    get_reusable_executor().shutdown(wait=True)
    
    #call NN segmentation
    if inputStruct['applyNeuralNetSegmentation']:
        preprocessNNFull(inputStruct)  
        
    instruct2 = copy.deepcopy(inputStruct)    #create modified input struct so registration also crops/registers NN channels
    if instruct2['applyNeuralNetSegmentation']:
        instruct2['channels'].append('NNseg')
        if instruct2['saveNNProbMap']: instruct2['channels'].append('NNprob')
        
    ## this loop is parallel - registration
    if instruct2['applyImageRegistration']:
        p2 = Parallel(n_jobs=instruct2['CPU_NUMs'])
        results = p2((delayed(preprocessRegSubfolder)(instruct2, subfolderNow) for subfolderNow in dirList))
        p2._aborted = True
        get_reusable_executor().shutdown(wait=True)

    #serial version
    #for subfolderNow in dirList:
    #    preprocessImagesSubfolder(inputStruct, subfolderNow
        

def preprocessFFSubfolder(inputStruct, subfolderNow):
    if inputStruct['quite'] == False: print('Start processing', subfolderNow) 
    # create output directories
    inputPath = os.path.join(inputStruct['inputParentPath'], subfolderNow)
    intermediatePath = inputPath
    if inputStruct['applyFlatFielding']:
        intermediatePath = os.path.join(inputStruct['outputParentPath'], subfolderNow+'FlatFielding') # will be deleted after image registration
        if os.path.isdir(intermediatePath) == False:
            try: os.makedirs(intermediatePath)
            except: exitMsg('Cannot create the directory: '+outputPath)
    outputPath = os.path.join(inputStruct['outputParentPath'], subfolderNow+'Registration')
    if os.path.isdir(outputPath) == False:
        try: os.makedirs(outputPath)
        except: exitMsg('Cannot create the directory: '+outputPath)

    # get the frames for subfolderNow
    frames = {}
    for ch in inputStruct['channels']:
        allfiles = os.listdir(inputPath)
        imgList = [f for f in allfiles if (f.startswith('.') == False) and os.path.isfile(os.path.join(inputPath,f)) and (ch in f)]
        imgList.sort()
        frames[ch] = [int(re.split('_',x)[1]) for x in imgList]

    if len(inputStruct['processFrames']) == 0:
        keepFrames = frames[inputStruct['channels'][0]]
    elif all(x >= 0 for x in inputStruct['processFrames']):
        keepFrames = [x for x in frames[inputStruct['channels'][0]] if x in inputStruct['processFrames']]
    elif all(x < 0 for x in inputStruct['processFrames']):
        keepFrames = [x for x in frames[inputStruct['channels'][0]] if -x not in inputStruct['processFrames']]
    else:
        exitMsg('processFrames cannot have both values >=0 and values <0.')

    #check whether keepFrames present in every channel
    for ch in inputStruct['channels']:
        if set(keepFrames).issubset(frames[ch]) == False:
            print(ch, ' channel is not in every relevant frame in ', keepFrames)
            return


    # call flatFielding function
    if inputStruct['applyFlatFielding']:
        if inputStruct['quite'] == False: print('FlatFielding starts for', subfolderNow) 
        if inputStruct['UseSingleFrame']:
            flatFieldingOneImage(inputStruct, inputPath, intermediatePath, keepFrames)
        else:
            flatFielding(inputStruct, inputPath, intermediatePath, keepFrames)
        if inputStruct['quite'] == False: print('FlatFielding Done for', subfolderNow) 

def preprocessNNFull(inputStruct) :
    #call NN segmentation
    if inputStruct['applyNeuralNetSegmentation']:
        if inputStruct['quite'] == False: print('Neural Net Segmentation starting!') 
        #multiprocessing.freeze_support()
        p = multiprocessing.Process(target=useNNFull,args=(inputStruct,))
        p.start() 
        p.join()
        #useNNFull(inputStruct)  

def preprocessRegSubfolder(instruct2, subfolderNow):    
    if instruct2['quite'] == False: print('Back to processing', subfolderNow) 
    # create output directories
    inputPath = os.path.join(instruct2['inputParentPath'], subfolderNow)
    intermediatePath = inputPath
    if instruct2['applyFlatFielding']:
        intermediatePath = os.path.join(instruct2['outputParentPath'], subfolderNow+'FlatFielding') # will be deleted after image registration
        if os.path.isdir(intermediatePath) == False:
            try: os.makedirs(intermediatePath)
            except: exitMsg('Cannot create the directory: '+outputPath)
    outputPath = os.path.join(instruct2['outputParentPath'], subfolderNow+'Registration')
    if os.path.isdir(outputPath) == False:
        try: os.makedirs(outputPath)
        except: exitMsg('Cannot create the directory: '+outputPath)
    
    print(intermediatePath)

    # get the frames for subfolderNow
    frames = {}
    for ch in instruct2['channels']:
        allfiles = os.listdir(intermediatePath)
        imgList = [f for f in allfiles if (f.startswith('.') == False) and os.path.isfile(os.path.join(intermediatePath,f)) and (ch in f)]
        imgList.sort()
        frames[ch] = [int(re.split('_',x)[1]) for x in imgList]

    if len(instruct2['processFrames']) == 0:
        keepFrames = frames[instruct2['channels'][0]]
    elif all(x >= 0 for x in instruct2['processFrames']):
        keepFrames = [x for x in frames[instruct2['channels'][0]] if x in instruct2['processFrames']]
    elif all(x < 0 for x in instruct2['processFrames']):
        keepFrames = [x for x in frames[instruct2['channels'][0]] if -x not in instruct2['processFrames']]
    else:
        exitMsg('processFrames cannot have both values >=0 and values <0.')

    #check whether keepFrames present in every channel
    for ch in instruct2['channels']:
        if set(keepFrames).issubset(frames[ch]) == False:
            print(ch, ' channel is not in every relevant frame in ', keepFrames)
            return
            
    # registration and cropping for every channel
    if instruct2['applyImageRegistration']:
        
        # note that imgSizesAll=='same' and fracAreaAlign==0 wouldnt change anything about the images.
        imgSizesAll = 'same'
        if imgSizesAll == 'same' and instruct2['fracAreaAlign'] == 0:
            exitMsg('imgSizesAll of \'same\' with fracAreaAlign of 0 is stupid.')

        # calculate and apply registration and cropping for the first channel
        if instruct2['quite'] == False: print('Register for first channel Starts for', subfolderNow) 
        (idxStart, imgSize, shifts, status) = registerAndCropOneChannel(intermediatePath, outputPath, instruct2['channels'][0], keepFrames, imgSizesAll, instruct2['fracAreaAlign'])

        if status != '':
            print(status)
            return

        # apply registration-based cropping to other channels
        for i in range(1, len(instruct2['channels'])):
            if instruct2['quite'] == False: print('Register for Channel', instruct2['channels'][i], 'starts for', subfolderNow) 
            registerAndCropOneChannelApply(intermediatePath, outputPath, instruct2['channels'][i], keepFrames, idxStart, imgSize)

        #save the preprocessing data. 
        json.dump({'inputStruct':instruct2, 'idxStart':idxStart.tolist(), 'imgSize':imgSize.tolist(), 'shifts':shifts.tolist()}, open(os.path.join(outputPath, 'preprocessingMetadata.txt'), 'w'))

        #delete flatfielding directory, i.e intermediatePAth
        
        if instruct2['applyFlatFielding']:
            try:
                shutil.rmtree(intermediatePath)
            except:
                print('Cannot delete the flatfielding output directory:', intermediatePath)   


def preprocessImagesCaller(inputStruct):
    # call the mother function
    inputStruct = checkInputParam(inputStruct)
    callPreprocessImagesSubfolder(inputStruct)
