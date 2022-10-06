from pathlib import Path
import skimage.io as skio
import collections
from joblib import Parallel, delayed
import multiprocessing
import os
from loky import get_reusable_executor
from natsort import natsorted
import shutil

def bigLoop(struct1,posL,pathIn,pathOut):
    print('Reorganizing Position ' + str(posL))
    pfoldname = 'Pos'+str(posL-struct1['Position'][0]+struct1['Position'][1])
    #print(pfoldname)
    #print(posL)
    #print(struct1['Position'][1])
    PosFold = pathOut / pfoldname
    Path.mkdir(PosFold,parents=True, exist_ok=True)
    for b in range(len(struct1['Ch'])):
    #for b in range(2,4):
        for c in struct1['fList']:
            imname = struct1['EP'] +'_w'+str(b+1)+struct1['Ch'][b]+'_s'+str(posL)+'_t'+str(c)+'.TIF'
            im1 = skio.imread(str(pathIn / imname))
            imnameout = 'Img_'+str(c-1).zfill(9)+'_'+struct1['Ch'][b]+'_000.png'
            skio.imsave(str(PosFold / imnameout),im1,check_contrast=False)
            #with open(str(pathIn)+'/'+EP+'_w'+str(b+1)+Ch[b]+'_s'+str(PosL)+'_t'+str(c)+'.tif','rb') as fin:
              #  with open(PosFold+'/Img_'+str(c).zfill(9)+'_'+Ch[b]+'_000.png','wb') as fout:
                #    copyfileobj(fin,fout,16*1024*1024)


def bigLoopNoTime(struct1,posL,pathIn,pathOut):
    print('Reorganizing Position ' + str(posL))
    pfoldname = 'Pos'+str(posL-struct1['Position'][0]+struct1['Position'][1])
    #print(pfoldname)
    #print(posL)
    #print(struct1['Position'][1])
    PosFold = pathOut / pfoldname
    Path.mkdir(PosFold,parents=True, exist_ok=True)
    for b in range(len(struct1['Ch'])):
    #for b in range(2,4):
            imname = struct1['EP'] +'_w'+str(b+1)+struct1['Ch'][b]+'_s'+str(posL)+'.TIF'
            im1 = skio.imread(str(pathIn / imname))
            imnameout = 'Img_'+str(0).zfill(9)+'_'+struct1['Ch'][b]+'_000.png'
            skio.imsave(str(PosFold / imnameout),im1,check_contrast=False)
            
def PosCat(PosStruct):
    PosPerWell = PosStruct['PosPerWell']
    IF = PosStruct['ImgDir']
    a = natsorted(os.listdir(IF))
    channels = PosStruct['Ch']
    totalNumIn = int(sum(os.path.isdir(os.path.join(IF,i)) for i in a))
    totalNumOut = int(totalNumIn/PosPerWell)
    well = 1
    for i in range(0,totalNumOut):
        pos = 1
        fname = 'Temp' + str(well)
        imFout = Path(IF) / fname
        imFout.mkdir(parents=True, exist_ok=True)
        for j in range(0,PosPerWell):
            imFin = os.path.join(IF,a[pos*well - 1])
            for k in range(0,len(channels)):
                imName = 'Img_000000000_' + str(channels[k]) + '_000.png'
                imIn = str(Path(imFin) / imName)
                imNameOut = 'Img_'+str(pos-1).zfill(9)+'_'+ str(channels[k]) +'_000.png'
                imOut = str(imFout / Path(imNameOut))
                im1 = skio.imread(imIn)
                skio.imsave(imOut,im1,check_contrast=False)
            pos = pos+1
        well = well + 1
    for fnameX in os.listdir(IF):
        if fnameX.startswith("Pos"):
            shutil.rmtree(os.path.join(IF,fnameX))
    for t in range(0,totalNumOut):
        tname = 'Temp' + str(t+1)
        pname = 'Pos' + str(t+1)
        shutil.move(os.path.join(IF,tname),os.path.join(IF,pname))

            
def ReOrgMetFull(struct1):

    pathIn = Path(struct1['IP'])
    pathOut = Path(struct1['OF'])

    pathOut.mkdir(parents=True, exist_ok=True)
    tFrames = collections.Counter(pathIn.name for pathIn in pathIn.glob('*'+struct1['EP']+'*'+struct1['Ch'][0]+'*s1_' + '*'))
    tFrames2 = collections.Counter(pathIn.name for pathIn in pathIn.glob('*'+struct1['EP']+'*'+struct1['Ch'][0]+'*s1.' + '*'))
    if len(tFrames2) == 1:
        print('Found single timepoint, copying')
        mode = 1
        TP = collections.Counter(pathIn.name for pathIn in pathIn.glob('*'+struct1['EP']+'*'+struct1['Ch'][0]+'*'))
    elif len(tFrames) > 1:
        mode = 2
        TP = collections.Counter(pathIn.name for pathIn in pathIn.glob('*'+struct1['EP']+'*'+struct1['Ch'][0]+'*t1.*'))
        print('Found' + str(len(tFrames)) + ' ' + 'timepoints and' + str(len(TP)) + ' ' + 'Positions, copying')
    else:
        print('Error - no images found in ScopeData folder')


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
    struct1['plist'] = [*range(firstPos,MaxPos)]
    struct1['fList'] = [*range(struct1['Image'][0],maxFrames)]
    
    if struct1['numCPU'] == 0: struct1['numCPU'] = multiprocessing.cpu_count()

    if mode == 2:
        p2 = Parallel(n_jobs=struct1['numCPU'])
        results = p2((delayed(bigLoop)(struct1, posx,pathIn,pathOut) for posx in range(firstPos,MaxPos+1))) #['pList']))
        p2._aborted = True
        if os.name == 'posix':
            get_reusable_executor().shutdown(wait=True)
    if mode == 1:
        p2 = Parallel(n_jobs=struct1['numCPU'])
        results = p2((delayed(bigLoopNoTime)(struct1, posx,pathIn,pathOut) for posx in range(firstPos,MaxPos+1))) #['pList']))
        p2._aborted = True
        if os.name == 'posix':
            get_reusable_executor().shutdown(wait=True)
