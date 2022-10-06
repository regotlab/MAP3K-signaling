#ReOrgMetPythonCaller

import sys
#sys.path.append("/home/regotlab/Documents/ImageAnalysisPython/")

from src.ReOrgMet import *

struct1 = {}


struct1['EP'] = "Exp2" #Experiment Prefix
struct1['IP'] = r'Z:\ScopeData\Images\Connor\201113_ZAK_mut'
struct1['OF'] = r'C:\Users\RegotLab\Documents\TestImages' #Output Folder
struct1['Ch'] = ["Far-red"] #Channel List
struct1['Image'] = (1,0)
struct1['Position'] = (10,0)
struct1['LastImg'] = 145
struct1['LastPos'] = 17
struct1['numCPU'] = 8


#detect timed vs untimed, properties/defaults. struct1['LastPos'], lastimg
ReOrgMetFull(struct1)


