#ReOrgMetPythonCaller

import sys
#sys.path.append("/home/regotlab/Documents/ImageAnalysisPython/")

from src.ReOrgMet import *

struct1 = {}


struct1['EP'] = "Exp1" #Experiment Prefix
struct1['IP'] = r'X:\ScopeData\Images\Tim\200309\MEK2_MKK3_DD_Co_Inh'
struct1['OF'] = r'C:\LocalAnalysisC\Tim\200309_test\RawImages' #Output Folder
struct1['Ch'] = ["Far-red","CFP","YFP"] #Channel List
struct1['Image'] = (1,0)
struct1['Position'] = (1,0)
struct1['LastImg'] = 10
struct1['LastPos'] = 5
struct1['numCPU'] = 60


#detect timed vs untimed, properties/defaults. struct1['LastPos'], lastimg
ReOrgMetFull(struct1)


