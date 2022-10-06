'''


'''
from __future__ import print_function
from __future__ import division

from builtins import range
from past.utils import old_div
import re
import os
import math
import numpy as np
from PIL import Image
from PIL import ImageMath
from scipy import ndimage
from scipy import misc
import scipy
import skimage.io as skio
from skimage.feature import register_translation
from timeit import default_timer as timer
from skimage.registration import phase_cross_correlation


def getFramesFromFilenames(imgNames, keepFrames):
    imgs = []
    for img in imgNames:
        temp = re.split('_',img)
        frm = int(temp[1])
        if frm in keepFrames: imgs.append(img)
    return imgs

def isoData(img, logArg):
	if logArg == 'log':
		img = np.log(np.double(img))	
	maxIter = 50  ##1e2
	tol = 1e-4 ##1e-6
	img = np.array(img)
	imgFlat = img.flatten(order='F')
	ii = 0
	thresh = np.zeros(maxIter+1) 
	thresh[ii] = np.mean(imgFlat)
	end = ii
	while ii<maxIter:
		imgBw = img > thresh[ii]
		bwf = imgBw.flatten(order = 'F')
		mbt = np.mean(np.array([imgFlat[x] for x in range(0,len(bwf)) if bwf[x] == False]))
		mat = np.mean(np.array([imgFlat[x] for x in range(0,len(bwf)) if bwf[x] == True]))
		thresh[ii+1] = 0.5*(mbt + mat)
		end = ii+1
		if thresh[ii+1] - thresh[ii] > tol:
			ii = ii + 1
		else:
			break		
	level = thresh[end]
	if logArg == 'log':
		level = math.exp(level)
	return (level, imgBw+0) #converting boolean array to int

def dftregistration(buf1ft,buf2ft,usfac=1):
	#Whole-pixel shift - Compute crosscorrelation by an IFFT and locate the peak
	output = []
	col_shift = 0
	row_shift = 0
	diffphase = 0
	if usfac == 1:
		m,n = buf1ft.shape
		CC = np.fft.ifft2(buf1ft * np.conjugate(buf2ft))
		CC= CC.real
		max1 = np.max(CC,axis=0)
		loc1 = np.argmax(CC,axis=0)
		max2 = np.max(max1,axis=0)
		loc2 = np.argmax(max1,axis=0)
		rloc=loc1[loc2]
		cloc=loc2
		CCmax=CC[rloc][cloc]
		rfzero = old_div(np.sum(np.abs(buf1ft)*np.abs(buf1ft)),(m*float(n)))
		rgzero = old_div(np.sum(np.abs(buf2ft)*np.abs(buf2ft)),(m*float(n))) 
		error = 1.0 - old_div(CCmax*np.conjugate(CCmax),(rgzero*float(rfzero)))
		error = np.sqrt(np.abs(error))
		diffphase = np.arctan2(CCmax.imag,CCmax.real)
		md2 = int(old_div(m,2)) 
		nd2 = int(old_div(n,2))
		row_shift = rloc 
		if rloc > md2:
			row_shift = rloc - m 
		col_shift = cloc 
		if cloc > nd2:
			col_shift = cloc - n 
		output = [error,diffphase,row_shift,col_shift]
	##for usfac != 1, there are other codes in dftregistration.m
	#Compute registered version of buf2ft
	Greg = 0
	if usfac > 0:
		nr,nc = buf2ft.shape
		Nr = np.fft.ifftshift(np.arange(-int(nr/2.0),np.ceil(nr/2.0)))
		Nc = np.fft.ifftshift(np.arange(-int(nc/2.0),np.ceil(nc/2.0)))
		Nc,Nr = np.meshgrid(Nc,Nr)
		Greg = buf2ft * np.exp (1j * 2 * np.pi * (-row_shift * Nr/float(nr) - col_shift * Nc/ float(nc)))
		Greg = Greg * np.exp(1j * diffphase)
	else:
		if usfac == 0: Greg = buf2ft * np.exp(1j * diffphase)
	return (output, Greg)

def imtranslate(I, translation, F):
	Iout = ndimage.interpolation.shift(I, translation, mode='constant',cval = F)
	return Iout

####################################################

def registerAndCropOneChannelApply(inputPath, outputPath, imgKey, keepFrames, idxStart, imgSize):
    #start = timer()
    
    imgList = os.listdir(inputPath)
    imgNamesAll = [x for x in imgList if imgKey in x]
    imgNamesAll.sort()

    if len(keepFrames) == 0:
        imgNames = imgNamesAll
    else:
    	imgNames = getFramesFromFilenames(imgNamesAll, keepFrames)

    for i in range(0, len(imgNames)):
        #img = mpl.imread(os.path.join(inputPath, imgNames[i]))
        img=skio.imread(os.path.join(inputPath, imgNames[i]))
        imgRegCrop = img[int(idxStart[i][0])-1:int(idxStart[i][0])+int(imgSize[0])-1,int(idxStart[i][1])-1:int(idxStart[i][1])+int(imgSize[1])-1]
		#misc.imsave(os.path.join(outputPath, imgNames[i]), imgRegCrop) 
#        scipy.misc.toimage(imgRegCrop, mode = 'I', high = np.max(imgRegCrop), low = np.min(imgRegCrop)).save(path)
        #ImageMath.eval("convert(a,'I')",a = Image.fromarray(imgRegCrop,mode ='I')).save(path)
        try: 
            skio.imsave(os.path.join(outputPath, imgNames[i]),imgRegCrop,check_contrast=False)
        except ValueError:
            print(imgRegCrop)
            print('Error - cannot save registered image')
            #print(
            #pass
    end = timer()
    #print(end-start)




def registerAndCropOneChannel(inputPath, outputPath, imgKey, keepFrames, imgSizesAll, fracAreaAlign):
    start = timer()
    #using fracAreaAlign of 0 is not recommended. it does no registration or cropping, but just pads with the median.
    # fracAreaAlign of 0 saves no time compared to using 0.5.
    # note that imgSizesAll=='same' and fracAreaAlign==0 wouldn't change anything about the images.

    thresholdLogArg = 'log'
    if imgSizesAll == 'same' and fracAreaAlign==0:
        exitMsg('imgSizesAll of \'same\' with fracAreaAlign of 0 is stupid.')
    #s1 = timer()
    #print("s1")
    #print(s1-start)
    # get the file names and initialize variables
    allImgList = os.listdir(inputPath)
    imgNamesAll = [x for x in allImgList if imgKey in x]
    imgNamesAll.sort()
    #s2 = timer()
    #print("s2")
    #print(s2-start)

    imgNames = []
    if len(keepFrames) == 0:
        imgNames = imgNamesAll
    else:
        imgNames = getFramesFromFilenames(imgNamesAll, keepFrames)

    if len(imgNames) == 0: return ([],[],[],'No image found for channel '+imgKey)
    imgNamesPath = []
    for i in imgNames: imgNamesPath.append(os.path.join(inputPath,i))

    #s3 = timer()
    #print("s3")
    #print(s3-start)
    
    nFrames = len(imgNames)
    shifts = np.zeros((nFrames, 2))

    s4 = timer()
    #print("s4")
    #print(s4-start)
    
	## figure out image sizes
    if imgSizesAll == 'same':
        sizeImg = np.array(skio.imread(imgNamesPath[0]).shape)
        imgSizesSeries = np.tile(sizeImg, (len(imgNames), 1))

    elif imgSizesAll == 'various': # this is inefficient. why don\'t you know the image sizes?
        imgSizesSeries = []
        for i in range(0, nFrames):
            imgSizesSeries.append(skio.imread(imgNamesPath[0]).shape)
        imgSizesSeries = np.array(imgSizesSeries)
    else:
        imgSizesSeries = imgSizesAll
        
    ####
    if fracAreaAlign!=0:  # perform image registration and cropping
        fracAlign = old_div(float(math.ceil(2*fracAreaAlign)), 2) # given values >0 and <=0.5 become 0.5, given values >0.5 become 1
    else:
        return ([],[],[],'Please use fracAreaAlign != 0 ')

    # calculate nOffset and nAlign
    minImgSize =  np.min(imgSizesSeries, axis = 0)

    if fracAlign==1:
        nOffset = [0, 0] # for rows and columns
        nAlign = minImgSize
    elif fracAlign==0.5:
        nOffset = np.round(old_div(minImgSize,4))
        nAlign = np.round(old_div(minImgSize,2))
    else:
        print('Considered fracAlign = 1')
        nOffset = [0, 0] # for rows and columns
        nAlign = minImgSize
        
    s5 = timer()
    #print("s5")
    #print(s5-start)

    # calculate the shifts for each image in the series
    ii= 0
    img2Full = skio.imread(imgNamesPath[ii])
    (imgNamesPath)
    img2 = img2Full[int(nOffset[0])-1:int(nOffset[0])+int(nAlign[0])-1, int(nOffset[1])-1:int(nOffset[1])+int(nAlign[1])-1]
    levelThr, img2Comp = isoData(img2, thresholdLogArg)
    img2CompX = img2Comp
    img2Comp = ndimage.binary_opening(img2Comp, structure=np.ones((3,3)),iterations=2).astype(np.int)
    #print(img2Comp)
    #print(type(img2Comp))
    #print(np.max(img2Comp))
    #print(img2Comp.shape)
    #print(img2Full.shape)
    #print(img2.shape)
    #print(img2CompX.shape)

    
    
    #s6 = timer()
    #print("s6")
    #print(s6-start)
        
    #img2Comp = imopen(img2Comp, strel('disk', 3));
    for ii in range(1,nFrames):
        #shifts[ii] = [regData[2],regData[3]]
        a1 = skio.imread(imgNamesPath[ii-1])
        a2 = skio.imread(imgNamesPath[ii])
        #s3, s4, s5 = register_translation(a1,a2)
        s3, s4, s5 = phase_cross_correlation(a1,a2)
        shifts[ii] = s3 + shifts[ii-1]
        #print(shifts[ii])


        # #if fracAlign==1:
            # img2 = imtranslate(img2, shifts[ii], float(np.median(img2))) # output will still be same class as original img2
        # #else:  # if shift is too big
            # if (nOffset[0]-shifts[ii][0]<1 or nOffset[1]-shifts[ii][1]<1) or ((nOffset[0]+nAlign[0]-1- shifts[ii][0])>imgSizesSeries[ii][0]) or ((nOffset[1]+nAlign[1]-1- shifts[ii][1])>imgSizesSeries[ii][1]):
                # img2Full = imtranslate(img2Full, shifts[ii], float(np.median(img2)))
                # print('we here')
            # img2 = img2Full[int(nOffset[0])-int(shifts[ii][0])-1:int(nOffset[0])+int(nAlign[0])-int(shifts[ii][0])-1, int(nOffset[1])-int(shifts[ii][1])-1:int(nOffset[1])+int(nAlign[1])-int(shifts[ii][1])-1]
            
        #levelThr, img2Comp = isoData(img2, thresholdLogArg)
        #img2Comp = ndimage.binary_opening(img2Comp, structure=np.ones((3,3)),iterations=2).astype(np.int)
        #img2Comp = imopen(img2Comp, strel('disk', 3))

    #s7 = timer()
    #print("s7")
    #print(s7-start)        
    # calculate limits
    maxShifts = np.max(shifts, axis = 0)
    idxStart = np.zeros([nFrames, 2])
    imgSize = np.zeros([2])
    for i in range(0,2):
        idxStart[:,i] =  maxShifts[i]+1 - shifts[:,i]
        imgSize[i] = np.min(imgSizesSeries[:,i] + shifts[:,i]) - maxShifts[i] # should work even if imgSizesAll=='same'

    # apply the registration and cropping
    #s8 = timer()
    #print("s8")
    #print(s8-start)
    for ii in range(0,nFrames):
        img = skio.imread(os.path.join(inputPath, imgNames[ii]))
        imgRegCrop = img[int(idxStart[ii][0])-1:int(idxStart[ii][0])+int(imgSize[0])-1,int(idxStart[ii][1])-1:int(idxStart[ii][1])+int(imgSize[1])-1]
        #misc.imsave(os.path.join(outputPath, imgNames[ii]), imgRegCrop) 
#      scipy.misc.toimage(imgRegCrop, mode = 'I', high = np.max(imgRegCrop), low = np.min(imgRegCrop)).save(path)
        try:
            skio.imsave(os.path.join(outputPath, imgNames[ii]),imgRegCrop,check_contrast=False)
        except ValueError:
            pass

    #s9 = timer()
    #print("s9")
    #print(s9-start)
    #print imgSize, shifts, idxStart
    return (idxStart, imgSize, shifts, '')

    ''' #Code for fracAreaAlign == 0; as we define fracAreaAlign = 0.5; we aparently no need this!
    else # no alignment, just pad the images with the median
        imgSize = max(imgSizesSeries, [], 1);
        for ii=1:nFrames
            img = imread(fullfile(inputPath, imgNames{ii}))
            padVal = median(img(:))
            imgPadded = padarray(img, imgSize-size(img), padVal, 'post')
            imwrite(imgPadded, fullfile(outputPath, imgNames{ii}))
            ii;end;1;end
    '''

