from pathlib import Path
import skimage.io as skio
import collections
from joblib import Parallel, delayed
import multiprocessing
import os

def bigLoop(struct1,posL,pathIn,pathOut):
    print('Reorganizing Position ' + str(posL))
    pfoldname = 'Pos'+str(posL-struct1['Position'][0]+struct1['Position'][1])
    PosFold = pathOut / pfoldname
    Path.mkdir(PosFold,parents=True, exist_ok=True)
    for b in range(len(struct1['Ch'])):
    #for b in range(2,4):
        for c in struct1['fList']:
            imname = struct1['EP'] +'_w'+str(b+1)+struct1['Ch'][b]+'_s'+str(posL)+'_t'+str(c)+'.tif'
            im1 = skio.imread(str(pathIn / imname))
            imnameout = 'Img_'+str(c-1).zfill(9)+'_'+struct1['Ch'][b]+'_000.png'
            skio.imsave(str(PosFold / imnameout),im1,check_contrast=False)
            #with open(str(pathIn)+'/'+EP+'_w'+str(b+1)+Ch[b]+'_s'+str(PosL)+'_t'+str(c)+'.tif','rb') as fin:
              #  with open(PosFold+'/Img_'+str(c).zfill(9)+'_'+Ch[b]+'_000.png','wb') as fout:
                #    copyfileobj(fin,fout,16*1024*1024)

def ReOrgMetFull(struct1):

    pathIn = Path(struct1['IP'])
    pathOut = Path(struct1['OF'])

    pathOut.mkdir(parents=True, exist_ok=True)
    tFrames = collections.Counter(pathIn.name for pathIn in pathIn.glob('*'+struct1['EP']+'*'+struct1['Ch'][0]+'*s1_*'))
    if len(tFrames) == 1:
        print('Found single timepoint, copying')
        TP = collections.Counter(pathIn.name for pathIn in pathIn.glob('*'+struct1['EP']+'*'+struct1['Ch'][0]+'*'))
    elif len(tFrames) > 1:
        TP = collections.Counter(pathIn.name for pathIn in pathIn.glob('*'+struct1['EP']+'*'+struct1['Ch'][0]+'*t1.*'))
        print('Found' + str(len(tFrames)) + ' timepoints, copying')
    else:
        print('Error - no images found in ScopeData folder')
        exit()


    if struct1['LastPos'] > 0:
        MaxPos = struct1['LastPos'] #- struct1['Position'][0] + 1
    else:
        MaxPos = len(TP)
    if struct1['LastImg'] > 0:
        maxFrames = struct1['LastImg'] #- struct1['Image'][0] + 1
    else:
        maxFrames = len(tFrames)
        
    firstPos = (struct1['Position'][0])

    
    #struct1['pList'] = TP[struct1['Position'][0]-1:MaxPos]
    struct1['plist'] = [*range(firstPos,MaxPos+1)]
    struct1['fList'] = [*range(struct1['Image'][0],maxFrames+1)]
    
    if struct1['numCPU'] == 0: struct1['numCPU'] = multiprocessing.cpu_count()

     
    p2 = Parallel(n_jobs=struct1['numCPU'])
    results = p2((delayed(bigLoop)(struct1, posx,pathIn,pathOut) for posx in range(firstPos,MaxPos+1))) #['pList']))
    p2._aborted = True
    if os.name == 'posix':
        get_reusable_executor().shutdown(wait=True)