import sys
#sys.path.append(r'C:\Users\Tim\Documents\ImageAnalysis\ImageAnalysisPython')

from src.trackOrganizeCpData import trackOrganizeCpDataDir

#parentPath = r'D:\LocalAnalysisD\Jose\201119_PGC1\Output'
parentPath = r'D:\LocalAnalysisD\Bryan\Ctest2'
cpDataFilename = 'cpData.mat'

# objects that you want organized. first element must correspond to the object used for tracking (usually nuclei).
# presumably you also saved these objects' label images as part of the pipeline.
objectSetNames = ['nuclei', 'cytoring']

subfolderNames = [] # if empty, then all subfolders will be analyzed

# tracking parameters
trackParam = {}
trackParam['maxdisp'] = [30,15] # The redius reduces by 0.95 and stops at 2
trackParam['mem'] = 3
trackParam['good'] = 20
trackParam['dim'] = 2
trackParam['quiet'] = 0

# output file's suffix
outputSuffix = 'Tracked'

# call the function
inputStruct = {}
inputStruct['parentPath'] = parentPath
inputStruct['cpDataFilename'] = cpDataFilename
inputStruct['objectSetNames'] = objectSetNames
inputStruct['subfolderNames'] = subfolderNames
inputStruct['trackParam'] = trackParam
inputStruct['outputSuffix'] = outputSuffix

trackOrganizeCpDataDir(inputStruct)
