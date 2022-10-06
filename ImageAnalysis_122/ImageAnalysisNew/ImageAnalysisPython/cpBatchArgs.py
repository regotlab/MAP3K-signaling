#!/usr/bin/python

# See readme.txt for instructions on how to run this on the server.
# See the cellProfiler folder for an example pipeline, which shows how to save images of objects.

cellProfilerPath = 'cellprofiler'
# if properly pip installed for version 3+, no need to specify path - just say 'cellprofiler'

pipelineFilepath = r'D:\LocalAnalysisD\Jose\20_12_21_Starved_PGC1\2color.cppipe'

inputParentPath = r'D:\LocalAnalysisD\Bryan\Test8\Images'

outputParentPath = r'D:\LocalAnalysisD\Bryan\Test8\Output'

outputFilename = 'cpData.mat'
# cellprofiler can save output as .mat (default) or .hdf5 (supported in 3.0+)

subfolderNames = []
# use an empty list [] if all subfolders should be analyzed.

frameFirstLast = []
# first and last frames to analyze, inclusive.
# every frame to analyze must have every channel that is used in loadimages in the pipeline.
# frame numbers are according to the image filenames (so zero-indexed).
# use an empty list [] if all images should be analyzed.

preClean = True
# preClean specifies whether the output subfolders should be deleted (if they exist) before calling CellProfiler.
# Setting preClean to True is the safer option, since CellProfiler sometimes has problems
# if there are already .tiff or cpData files in the output folders.
# Using preClean of True also prevents the program from calculating outline images of outline images.

runCellProfiler = True
# True or False, controls whether the cellprofiler pipeline is run.

runChannelImageCompression = True
# True or False, controls whether the compressed channel images are generated.

nMaxCores = 22
# set nMaxCores to a number greater than 0 and less than 8, if you want to be a good citizen
# and not hog all the CPUs on the front end of covertlab-cluster.
# 0 means no limit to the number of cores.
