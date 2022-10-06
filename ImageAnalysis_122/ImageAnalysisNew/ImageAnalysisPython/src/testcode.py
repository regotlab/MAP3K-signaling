import random
from skimage import io as skio
import pathlib
from pathlib import Path
import skimage.io as skio
import collections
import os
import shutil

def testMode(struct1,struct2,ExcludePos,numTestImages):
    pathIn = Path(struct1['IP'])
    pathOut = Path(struct1['OF'])

    pathOut.mkdir(parents=True, exist_ok=True)
    tFrames = collections.Counter(pathIn.name for pathIn in pathIn.glob('*'+struct1['EP']+'*'+struct1['Ch'][0]+'*s1_*'))
    if len(tFrames) == 1:
        print('Found single timepoint')
        TP = collections.Counter(pathIn.name for pathIn in pathIn.glob('*'+struct1['EP']+'*'+struct1['Ch'][0]+'*'))
    elif len(tFrames) > 1:
        TP = collections.Counter(pathIn.name for pathIn in pathIn.glob('*'+struct1['EP']+'*'+struct1['Ch'][0]+'*t1.*'))
        print('Found' + str(len(tFrames)) + ' ' + 'timepoints and' + str(len(TP)) + ' ' + 'Positions, copying')
    else:
        print('Error - no images found in ScopeData folder')
        exit()
        
    if struct1['LastPos']:
        MaxPos = int(struct1['LastPos']) #- struct1['Position'][0] + 1
    else:
        MaxPos = len(TP)
    if struct1['LastImg']:
        maxFrames = int(struct1['LastImg']) #- struct1['Image'][0] + 1
    else:
        maxFrames = len(tFrames)
        
    firstPos = (struct1['Position'][0])

    
    #struct1['pList'] = TP[struct1['Position'][0]-1:MaxPos]
    struct1['plist'] = [*range(firstPos,MaxPos+1)]
    struct1['fList'] = [*range(struct1['Image'][0],maxFrames+1)]
    
    
    #numPos = maxPos - minPos + 1
    #numFrames = maxFrame - minFrame + 1
    
    

    posList = []
    frameList = []
    
    if struct2['applyFlatFielding'] == True and struct2['UseSingleFrame'] == False:
        fflist = [*range(struct2['startFlatfieldPos'],struct2['endFlatfieldPos'])]
        for frn in range(len(fflist)):
            ExcludePos.append(fflist[frn])   
    
    
    print(pathOut)
    while len(posList) < numTestImages:
        a = random.randint(firstPos,MaxPos+1)
        b = random.randint(struct1['Image'][0],maxFrames+1)
        if a not in ExcludePos:   # and b is not in ExcludeFrame:
            posList.append(a)
            frameList.append(b)
    Channels = struct1['Ch']
    ExpPrefix = struct1['EP']
    print('Test images from positions:' + str(posList))
    print('Test image frames:' + str(frameList))
    txtname = str(pathOut / 'imageList.txt')
    f1 = open(txtname, 'w')
    for i in range(numTestImages):
        for c in range(len(Channels)):
            imN = ExpPrefix + '_w' + str(c+1) + Channels[c] + '_s' + str(posList[i]) + '_t' + str(frameList[i]) + '.TIF'
            imP = pathIn / pathlib.Path(imN)
            #outPath1 = pathOut / pathlib.Path('Pos' + str(posList[i])) 
            outPath1 = pathOut / 'Pos0'
            outPath1.mkdir(parents = True, exist_ok=True)
            outpath3 = 'Img_' + str(i).zfill(9) + '_' + Channels[c] + '_000.png'
            outpathwrite = outPath1 / outpath3
            f1.write(str(outpathwrite) + '\n')
            outPath2 = outPath1 / pathlib.Path('Img_' + str(i).zfill(9) + '_' + Channels[c] + '_000.png')
            img1 = skio.imread(imP)
            skio.imsave(str(outPath2),img1,check_contrast=False)
        if struct2['applyNeuralNetSegmentation']:
            outpath3 = 'Img_' + str(i).zfill(9) + '_' + 'NNseg' + '_000.png'
            outpathwrite = outPath1 / outpath3
            f1.write(str(outpathwrite) + '\n')


def testFromOrg(struct2,ExcludePos,numTestImages,firstPos,MaxPos,firstFrames,maxFrames):
 
    posList = []
    frameList = []
    rawDir = Path(struct2['inputParentPath'])
    testDir = Path(struct2['outputParentPath'])
    testDirPos = testDir / 'Pos0'
    if struct2['applyFlatFielding'] == True and struct2['UseSingleFrame'] == False:
        fflist = [*range(struct2['startFlatfieldPos'],struct2['endFlatfieldPos'])]
        for frn in range(len(fflist)):
            ExcludePos.append(fflist[frn])   
    
    print(firstPos)
    print(MaxPos)
    while len(posList) < numTestImages:
        a = random.randint(firstPos,MaxPos)
        b = random.randint(firstFrames,maxFrames)
        if a not in ExcludePos:   # and b is not in ExcludeFrame:
            posList.append(a)
            frameList.append(b)
    testDirPos.mkdir(parents=True, exist_ok=True)
    txtname = str(testDir / 'imageList.txt')
    f1 = open(txtname, 'w')
    Channels = struct2['channels']
    for i in range(numTestImages):
        for c in range(len(Channels)):
            img = frameList[i]
            pos = 'Pos' + str(posList[i])
            imIn = 'Img_' + str(img).zfill(9) + '_' + Channels[c] + '_000.png'
            imOut = 'Img_' + str(i).zfill(9) + '_' + Channels[c] + '_000.png'
            imN = rawDir / pos / imIn
            imO = testDir / 'Pos0' / imOut
            shutil.copyfile(str(imN),str(imO))
            f1.write(str(imO) + '\n')
        if struct2['applyNeuralNetSegmentation']:
            outpath3 = 'Img_' + str(i).zfill(9) + '_' + 'NNseg' + '_000.png'
            outpath = testDir / 'Pos0' / outpath3
            f1.write(str(outpath) + '\n')