'''



'''
import sys
sys.path.append("/home/Documents/ImageAnalysis/ImageAnalysisPython/")

from src.preprocessImages import *


inputStruct = {}
inputStruct['inputParentPath'] = r'C:\Users\RegotLab\VirtualBox VMs\LocalAnalysisC\Bryan\RawImages'
inputStruct['outputParentPath'] = r'C:\Users\RegotLab\VirtualBox VMs\LocalAnalysisC\Bryan\Images'


# if empty, all subfolders in the inputPath will be preprocessed
inputStruct['subfolderNames'] = []
inputStruct['channels'] = ["CFP","Far-red","TRITC","YFP"]

inputStruct['applyFlatFielding'] = False
inputStruct['prefix'] = 'Pos'
inputStruct['UseSingleFrame'] = False
#If UseSingleFrame == False, then define the start position and end position
inputStruct['startFlatfieldPos'] = 55
inputStruct['endFlatfieldPos'] = 58

inputStruct['applyImageRegistration'] = True

# if processFrames is empty, all frames will be processed.
# if processFrames has values greater than or equal to zero, only those frames will be processed.
# if processFrames has values less than zero, those frames will be ignored.
inputStruct['processFrames'] = []

#TRUE if no print statement
inputStruct['quite'] = False

#number of CPUs; 0 will consider all CPUs. FOR MACHINES WITH 64+ LOGICAL CORES, MANUALLY CAP THIS AT 60.
inputStruct['CPU_NUMs'] = 12

#Neural Net Segmentation settings
#Supply name of nuclear marker channel for NN to segment with, and file path to the keras .hdf5 model file
#Only turn on saveNNProbMap if you want the full 3-class (nucleus, boundary, background) raw probabilities. The masks will still save with this turned off.
inputStruct['applyNeuralNetSegmentation'] = True
inputStruct['nuclearMarkerChannel'] = 'Far-red'
inputStruct['neuralNetModelPath']  = r'C:\Users\RegotLab\Documents\ImageAnalysisPython\NNs\model.hdf5'

inputStruct['cell_min_size'] = 35
inputStruct['saveNNProbMap'] = False
inputStruct['useGPU'] = True 
##VIRTUAL MACHINES CANNOT ACCESS GPU. IF YOU WANT THE SPEED IMPROVEMENTS OF A GPU, RUN ON NATIVE MACHINE. 
##YOU PROBABLY WANT TO DO THIS IF YOU HAVE A FULL EXPERIMENT.

#### call the mother function
preprocessImagesCaller(inputStruct)
