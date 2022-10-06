import numpy as np
import pandas as pd
from pathlib import Path
from scipy import signal as sg
from datetime import datetime
import subprocess
import sklearn
from sklearn.linear_model import RidgeClassifierCV
from sklearn.pipeline import make_pipeline

from sktime.transformers.series_as_features.rocket import Rocket
from sktime.datasets.base import _load_dataset
from sktime.utils.load_data import load_from_tsfile_to_dataframe
import os

def mitosisRunner(inputDir):
    
    oList = os.listdir(inputDir)
    print(oList)
    fList = []
    for ti in oList:
        if os.path.isdir(os.path.join(inputDir,ti)): fList.append(ti)
    tnum = len(fList)
    idir2 = inputDir[:-1]
    print(tnum)
    #subprocess.call(['./run_makeMultiOnAll.sh','/usr/local/MATLAB/R2019b/',str(tnum),idir2])
    subprocess.run([r'C:\Users\RegotLab\Documents\ImageAnalysisPython\ImageAnalysis_122\ImageAnalysisNew\ImageAnalysisPython\src\makeMultiOnAll.exe',str(tnum),inputDir],shell=True)
    DATA_PATH = os.path.join(os.path.dirname(r'Y:\DocShare\Bryan\MitosisAnalysis\MeanXMulti.ts'))
    rocketv1(DATA_PATH,inputDir,tnum)
    frameGuesser2(inputDir,tnum)
    #strcomb2 = 'mitPredictorNew ' + str(num) + ' ' + inputDir
    subprocess.run([r'C:\Users\RegotLab\Documents\ImageAnalysisPython\ImageAnalysis_122\ImageAnalysisNew\ImageAnalysisPython\src\mitPredictorNew.exe',str(tnum),inputDir],shell=True)
    #subprocess.call(['./run_mitPredictorNew.sh','usr/local/MATLAB/R2019b/',str(tnum),inputDir])

def rocketv1(DATA_PATH,outputDir1,tnum):



    #print(os.path.isfile("Y:\DocShare\Bryan\MitosisAnalysis\MeanXMulti.ts"))

    X_train, y_train = load_from_tsfile_to_dataframe(
        os.path.join(DATA_PATH, "MeanXMulti.ts")
    )


    rocket = Rocket(num_kernels=10000)  # by default, ROCKET uses 10,000 kernels
    rocket.fit(X_train)
    X_train_transform = rocket.transform(X_train)

    classifier = RidgeClassifierCV(alphas=np.logspace(-3, 3, 10), normalize=False)
    classifier.fit(X_train_transform, y_train)

    #X_test, y_test = load_from_tsfile_to_dataframe(
    #    os.path.join(DATA_PATH, "MeanXMulti.ts")
    #)
    #X_test_transform = rocket.transform(X_test)

    st1 = outputDir1 + "\Pos"

    for i in range(1,tnum+1):
        st2 = st1 + str(i) + "Registration\\"
        print(st2)
        DATA_PATH2 = os.path.join(os.path.dirname(st2))
        X_test, y_test = load_from_tsfile_to_dataframe(
            os.path.join(DATA_PATH2, "MitosisClassifier.ts")
        )
        X_test_transform = rocket.transform(X_test)
        peachy = classifier.predict(X_test_transform)
        print(sum(peachy.astype(int)))
        saverPath = DATA_PATH2 + "\MitosisClassified.csv"
        np.savetxt(saverPath, peachy.astype('uint8'), delimiter=",")
        
def frameGuesser2(outputDir,tnum):
    import tensorflow as tf
    from tensorflow import convert_to_tensor as ctv

    gpu_options = tf.compat.v1.GPUOptions(visible_device_list="0")
    sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))

    tf.compat.v1.disable_eager_execution()

    #sess=tf.compat.v1.Session()
    

    fnameover = Path(outputDir)
    for i in range(1,tnum+1):
        print(i)

        ssimBig = np.array((0.1,0.1,0.1,0.1))
        ssimBig = np.reshape((ssimBig),(1,4,1,1))
        numPer = {}
        reference_ssim = [0.29, 4.5, 0.05, 15.5]
        reference_ssim = np.reshape(reference_ssim,(1,4,1,1))
        candDict3 = {}
        candDict4 = {}
        candBig = {}
        
        fname2 = 'Pos' + str(i) + 'Registration\MitosisClassifier.ts'
        fname1 = str(fnameover / fname2)
        fname3 = 'Pos' + str(i) + 'Registration\MitosisClassified.csv'
        fname4 = str(fnameover / fname3)
        data2 = pd.read_csv(fname4,header=None)
        
        data2 = data2.to_numpy()

        for z in range(0,len(data2)):

            if data2[z] == 1:
                #print('here')

                data1 = pd.read_csv(fname1,skiprows=6,sep='[:,]',header=None)

                MainArrayPre = data1.iloc[[z]].to_numpy()
                MainArray = MainArrayPre[0]
                tlength = int(len(MainArray)/3)
                tlength1 = tlength - 1
                tlength2 = tlength*2
                tlength21 = tlength2 - 1
                tlength3 = tlength*3
                tlength31 = tlength3 -1 
                aarr = MainArray[0:tlength1]
                #area input signal
                iarr = MainArray[tlength:tlength21] #intensity input signal
                divarr = MainArray[tlength2:tlength31]
                t = sg.argrelmin(aarr)
                barr = t[0]
                aarr2 = aarr
                aarr2[aarr2 == 0] = np.nan
                meanArea = np.nanmean(aarr2)
                iarr2 = iarr
                iarr2[iarr2 == 0] = np.nan
                meanInt = np.nanmean(iarr2)
                numMin = len(barr)
                cans = []
                for j in range(numMin):
                    valArea = aarr[barr[j]]
                    valInt = iarr[barr[j]]
                    arRatio1 = valArea/meanArea
                    if arRatio1 < 0.7:
                        cans.append(barr[j])
                numS = len(cans)
                ssim1 = np.zeros((numS,4,1,1))
                for k in range(numS):
                    ind1 = cans[k]
                    arRatio = aarr[ind1]/meanArea
                    intRatio = iarr[ind1]/meanInt
                    p3 = arRatio/intRatio
                    p4 = divarr[ind1]
                    ssim1[k,:,:,:] = np.reshape([arRatio, intRatio, p3, p4],(4,1,1))
                #print(ssim1.shape)
                #print(reference_ssim.shape)
                ssimBig = np.concatenate((ssimBig,ssim1),0)
                numPer[z] = numS
                candBig[z] = cans
                
                
                
        ssimBig = ssimBig[1:,:,:,:]
        print('ssimtime')
        print(datetime.now())
        ssimt = tf.image.ssim(ctv(ssimBig),ctv(reference_ssim),3,filter_size=1)
        ssimOut = ssimt.eval(session=sess)
        
        rxs = list(numPer.items())
        ind1 = 0
        
        for sN in range(0,len(rxs)):
            numEach = rxs[sN][1]
            ssO = ssimOut[ind1:numEach+ind1]
            
            tr_1 = rxs[sN][0]
            ind1 = ind1+numEach
            if len(ssO):
                guess = np.argmax(ssO)
                guessFr = candBig[tr_1][guess]
                candBig[tr_1] = cans
                candDict3[tr_1] = guessFr
                candDict4[tr_1] = ssO[guess]
            
                
        #print(ssO)
            
        probableTraces = []
        probableFrames = []
        probableValues = []
        pvals = list(candDict4.items())
        pframes = list(candDict3.items())
        for tv in range(0,len(candDict4)):
            if pvals[tv][1] > 0.7:
                probableTraces.append(pvals[tv][0])
                probableFrames.append(pframes[tv][1])
                probableValues.append(pvals[tv][1])
        fname9 = 'Pos' + str(i) + 'Registration\GuessedFrames.csv'
        fnamex = str(fnameover / fname9)
        print(fnamex)
        #fnamex = '/home/regotlab/Documents/temp3.csv'
        file1 = open(fnamex,"w+")
        for tt in range(0,len(probableTraces)):
            str1 = str(probableTraces[tt]) + ',' + str(probableFrames[tt]) + '\n'
            file1.write(str1)
        file1.close()