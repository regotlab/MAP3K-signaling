ReOrg = False #move files from ScopeData to local folder
preProcess = True #Flatfield, Neural Net, Register
cellprofiler = False #run CellProfiler
tracking = False #this is useless currently

testModeOn = False

##############
####Universal Variables
Channels = ["Far-red","TRITC","CFP","YFP"]
CPU_NUM = 25 #0 will consider all, CAP IT AT 60 IF YOUR COMPUTER HAS 64+ OR ELSE EVERYTHING BREAKS
quite = False

####Folders
reOrgInput = r'X:\ScopeData\Images\Tim\201108\Cell_Cycle_Test' #Scope Data Folder
reOrgOutput = r'D:\LocalAnalysisD\Jose\201119_PGC1\RawImages' #Local Analysis Folder
preprocessingInput = r'D:\LocalAnalysisD\Jose\201119_PGC1\RawImages'#leave empty to default to ReOrgOutput
preprocessingOutput = r'D:\LocalAnalysisD\Jose\201119_PGC1\Images'
cellprofilerInput = "" #leave empty to default to preprocessingOutput
cellprofilerOutput = ""

####REORG
ReOrgStruct = {} #DON'T EDIT THIS LINE
ReOrgStruct['EP'] = 'Exp2' #Experiment Prefix"
ReOrgStruct['Image'] = (299,298) #(x,y), first image number to read and first to write. Default is 1,0
ReOrgStruct['Position'] = (1,0) #(x,y), first position number to read and first to write. Default is 1,0
ReOrgStruct['LastImg'] = 301 #will default to final frame of ExpPrefix.
ReOrgStruct['LastPos'] = 63 #will default to final position of ExpPrefix.

####PREPROCESS
preprocessingStruct = {}
preprocessingStruct['applyImageRegistration'] = True
preprocessingStruct['applyNeuralNetSegmentation'] = True
preprocessingStruct['applyFlatFielding'] = True

preprocessingStruct['UseSingleFrame'] = False
preprocessingStruct['startFlatfieldPos'] = 48 #only necessary if not using single frame
preprocessingStruct['endFlatfieldPos'] = 50 #only necessary if not using single frame


    # if Frames is empty, all frames will be processed.
    # if Frames has values greater than or equal to zero, only those frames will be processed.
    # if Frames has values less than zero, those frames will be ignored.
preprocessingStruct['prefix'] = 'Pos'
preprocessingStruct['processFrames'] = [] 
preprocessingStruct['subfolderNames'] = []  #Leave empty to process all


preprocessingStruct['nuclearMarkerChannel'] = 'Far-red' #name of nuc marker channel to segment with
preprocessingStruct['cell_min_size'] = 28
preprocessingStruct['neuralNetModelPath'] = r'C:\Users\RegotLab\Documents\ImageAnalysisPython\NNs\model.hdf5' #filepath to keras .hdf5 model file
preprocessingStruct['saveNNProbMap'] = False #will save raw pixel classification (boundary, background, foreground) in addition to mask creation
preprocessingStruct['useGPU'] = True #DO NOT USE ON A VIRTUAL MACHINE

####CELLPROFILER
pipelineFilepath = r'C:\LocalAnalysisC\Tim\201108\Cell_Cycle_Test\CTA340pipe.cppipe' #filepath to .cppipe pipeline
outputFilename = 'cpData.mat' #
subfolderNames = [] #Leave empty to process all

    # first and last frames to analyze, inclusive.
    # every frame to analyze must have every channel that is used in loadimages in the pipeline.
    # frame numbers are according to the image filenames (so zero-indexed).
frameFirstLast = []  #Leave empty to process all

    # preClean specifies whether the output subfolders should be deleted (if they exist) before calling CellProfiler.
    # Setting preClean to True is the safer option, since CellProfiler sometimes has problems
    # if there are already .tiff or cpData files in the output folders.
    # Using preClean of True also prevents the program from calculating outline images of outline images.
preClean = True
runCellProfiler = True
runChannelImageCompression = True 

####TEST MODE
numTestImages = 5 #change this to change number of test images loaded into cellprofiler
ExcludePositions = [] #just use numbers, automatically includes flatfielding pos


############################
############CODE############
############################
import sys
sys.path.append(r'C:\Users\Tim\Documents\ImageAnalysis\ImageAnalysisPython')

from src.preprocessImages import *
from src.testcode import *
from src.ReOrgMet import *
from src.cpBatch import *
import subprocess
import time 
import pathlib
from pathlib import Path

if not preprocessingInput: preprocessingInput = reOrgOutput
if not cellprofilerInput: cellprofilerInput = preprocessingOutput

inputParentPath = cellprofilerInput


if not cellprofilerOutput:
    xp = Path(inputParentPath).parent
    outputParentPath = str(xp / 'Output')


outputParentPath = cellprofilerOutput

Frames = preprocessingStruct['processFrames']
if Frames and preProcess:
    c = [] 
    b = []
    for x in range(len(Frames)): 
        c.append(isinstance(Frames[x],int))
        if not min(c):
            print('Error - noninteger value in Frames')
            exit()
    for x in range(len(Frames)): 
        b.append(Frames[x]<0)
        if not min(b) == max(b):
            print('Error - cannot mix negative and positive values in Preprocessing frames')
            
if testModeOn == False:
    if ReOrg:
        print('Running ReOrg')
        ReOrgStruct['numCPU'] = CPU_NUM
        ReOrgStruct['IP'] = reOrgInput
        ReOrgStruct['OF'] = reOrgOutput
        ReOrgStruct['Ch'] = Channels
        ReOrgMetFull(ReOrgStruct)
        print('ReOrg succesful')
    if preProcess:
        preprocessingStruct['quite'] = quite
        print('Running preprocessing')
        preprocessingStruct['inputParentPath'] = preprocessingInput
        preprocessingStruct['outputParentPath'] = preprocessingOutput
        preprocessingStruct['CPU_NUMs'] = CPU_NUM
        preprocessingStruct['channels'] = Channels
        print(preprocessingStruct)
        preprocessImagesCaller(preprocessingStruct)
        print('Preprocessing successful')
    if cellprofiler:
        print('Running CellProfiler')
        cellProfilerPath = 'cellprofiler'
        nMaxCores = CPU_NUM
        if cellprofilerInput:
            inputParentPath = cellprofilerInput
        else:
            inputParentPath = preprocessingOutput
        if cellprofilerOutput:
            outputParentPath = cellprofilerOutput
        else:
            xp = Path(inputParentPath).parent
            outputParentPath = str(xp / 'Output')
        # s1 = "cellProfilerPath = 'cellProfiler'"
        # s2 = "\npipelineFilepath = '" + pipelineFilepath + "'"
        # s3 = "\ninputParentPath = '" + cpBatchInput + "'"
        # s4 = "\noutputParentPath = '" + cpBatchOutput + "'"
        # s5 = "\noutputFileName = '" + outputFilename + "'"
        # s6 = "\nsubFolderNames = " + str(Positions)
        # s7 = "\nframeFirstLast = " + str(Frames)
        # s8 = "\npreClean = " + str(preClean)
        # s9 = "\nrunCellProfiler = " + str(runCellProfiler)
        # s10 = "\nrunChannelImageCompression = " + str(runChannelImageCompression)
        # s11 = "\nnMaxCores = " + str(CPU_NUM)
        # fobj = open(r"cpBatchArgs_gen.py", "w+")
        # L = [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11]
        # fobj.writelines(L)
        # fobj.close()
        # import subprocess
        if __name__ == '__main__':
            #cpArgs = __import__(os.path.splitext(sys.argv[1])[0])

            #inputArgNames = [item for item in cpArgs if not item.startswith("__")]
            #inputArgValues = [getattr(cpArgs, varname) for varname in inputVarNames]

            #print(cpArgs.pipelineFilepath)
            #print(cpArgs.inputParentFilepath)
            
            print(pipelineFilepath)
            

            analyzeParentDirCp(pipelineFilepath, inputParentPath, outputParentPath,
            outputFilename, subfolderNames, frameFirstLast, cellProfilerPath,
            preClean, runCellProfiler, runChannelImageCompression, nMaxCores)
        #subprocess.call('python C:\\Users\\Tim\\Documents\\ImageAnalysis\\ImageAnalysisPython\\cpBatch.py StartToFinish.py')
        time.sleep(5)
        #print('CellProfiler batch successful')
        #print('Exiting!')
        
if testModeOn == True:
    print('Running Test Mode')
    print('Copying images')
    ReOrgStruct['numCPU'] = CPU_NUM
    ReOrgStruct['IP'] = reOrgInput
    ReOrgStruct['OF'] = reOrgOutput
    ReOrgStruct['Ch'] = Channels
    testMode(ReOrgStruct,preprocessingStruct,ExcludePositions,numTestImages)
    print('Preprocessing')
    preprocessingStruct['inputParentPath'] = str(Path(reOrgOutput) / 'test')
    preprocessingStruct['outputParentPath'] = str(Path(reOrgOutput) / 'test')
    preprocessingStruct['CPU_NUMs'] = CPU_NUM
    preprocessingStruct['channels'] = Channels
    preprocessingStruct['quite'] = quite
    preprocessingStruct['applyImageRegistration'] = False
    preprocessingStruct['applyFlatFielding'] = False 
    preprocessImagesCaller(preprocessingStruct)
    cpCommand = ['cellprofiler','-i',str(Path(reOrgOutput) / 'test')]
    print('Opening CellProfiler')
    subprocess.call(cpCommand)
