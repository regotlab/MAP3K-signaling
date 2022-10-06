import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from datetime import datetime
from pathlib import Path

import sys
sys.path.append('/home/regotlab/Documents/ImageAnalysis_122/ImageAnalysisNew/ImageAnalysisPython')

from src.preprocessImages import *
from src.testcode import *
from src.ReOrgMet import *
from src.cpBatch import *
from src.trackOrganizeCpData import trackOrganizeCpDataDir
import subprocess
import time 
import pathlib

from STFgui import Ui_MainWindow

from dialogPosCat import Ui_Dialog


def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    raw_input("Press key to exit.")
    sys.exit(-1)
    
import sys
sys.excepthook = show_exception_and_exit

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)
        self.BigStruct = {}
        
        self.setWindowTitle('wooo')
        self.checkBox.toggled.connect(self.ReOrg.setEnabled)
        self.checkBox_3.toggled.connect(self.Preprocessing.setEnabled)
        self.checkBox_2.toggled.connect(self.CellProfiler.setEnabled)
        self.checkBox_4.toggled.connect(self.Tracking.setEnabled)
        self.radioButton.toggled.connect(self.Tracking.setEnabled)
        self.radioButton.toggled.connect(self.CellProfiler.setEnabled)
        self.checkBox.toggled.connect(lambda: StructUpdate(self))
        
        #self.checkBox.toggled.connect(lambda: test2(self.BigStruct))
        self.next.clicked.connect(lambda: setter2(self))
        self.back.clicked.connect(lambda: setter1(self))
        
        self.runb.clicked.connect(lambda: StructUpdate(self))
        self.runb.clicked.connect(lambda: checkerSet(self))
        self.runb.clicked.connect(lambda: saver(self,2))
        self.runb.clicked.connect(lambda: mainRunner(self))

        
        self.b2_2.clicked.connect(lambda: openFiler(self,1))
        self.b2_1.clicked.connect(lambda: openFiler(self,2))

        
        self.Save.clicked.connect(lambda: StructUpdate(self))
        self.Save.clicked.connect(lambda: saver(self,1))
        self.Save_2.clicked.connect(lambda: saver(self,1))

        #self.runb.clicked.connect(lambda: mainRunner(self))
        #self.next.clicked.connect(self.tabWidget.setCurrentWidget(self.Settings_Tab))
        self.b1.clicked.connect(lambda: openFileBrowser(self, "b1"))
        self.b2.clicked.connect(lambda: openFileBrowser(self, "b2"))
        self.b3.clicked.connect(lambda: openFileBrowser(self, "b3"))
        self.b4.clicked.connect(lambda: openFileBrowser(self, "b4"))
        self.b5.clicked.connect(lambda: openFileBrowser(self, "b5"))
        self.b6.clicked.connect(lambda: openFileBrowser(self, "b6"))
        self.b7.clicked.connect(lambda: openFileBrowser(self, "b7"))
        self.b8.clicked.connect(lambda: openFileBrowser(self, "b8"))
        self.b9.clicked.connect(lambda: openFileBrowser(self, "b9"))
        self.help_2.clicked.connect(lambda: concatD(self))
        
    
def concatD(self):
        d = concatDx(self)
        d.show()
        
class concatDx(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, parent=None):

        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        
def checkerSet(self):
    if self.BigStruct['reOrg']:
        if not self.BigStruct['ReOrgMatrix']:
            print('Error - no Reorganizing Directory Set')
            self.BigStruct['Flag'] = 1
    if self.BigStruct['preprocess']:
        if not self.BigStruct['applyFlatFielding'] and not self.BigStruct['applyImageRegistration'] and not self.BigStruct['applyNeuralNetSegmentation']:
            print('No Preprocessing Steps selected')
        if ['applyNeuralNetSegmentation']:
            if not self.BigStruct['nuclearMarkerChannel']: 
                print('Error - no nuclear marker channel selected for Neural Net Segmentation')
                self.BigStruct['Flag'] = 1
            if not self.BigStruct['neuralNetModelPath']:
                print('Error - no Neural Net Model selected for Segmentation')
                self.BigStruct['Flag'] = 1
                
def saver(self,mode):
    if mode==1:
        self.saveName,_ = QFileDialog.getSaveFileName(self, "Save Config File As....", "/home/regotlab")
    if mode==2:
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d_%H%M%S")
        fname = "Settings_" + dt_string + ".txt"
        if self.Parent.text():
            self.saveName = str( Path(self.Parent.text()) / Path(fname) )
        else:
            self.saveName = str(Path('/tmp') / Path(fname))
    print(self.saveName)
    f1 = open(self.saveName, 'w')
    f1.write('Test Mode: ' + str(self.BigStruct['testModeOn']) + '\n')           
    f1.write('reOrg: ' + str(self.BigStruct['reOrg']) + '\n')
    f1.write('preprocess: ' + str(self.BigStruct['preprocess']) + '\n')
    f1.write('cellprofiler: ' + str(self.BigStruct['cellprofiler']) + '\n')
    f1.write('tracking: ' + str(self.BigStruct['tracking']) + '\n')
    
    f1.write('ReOrgOut: ' + str(self.BigStruct['ReOrgOut']))
    f1.write('PreprocessOut: ' + str(self.BigStruct['PreprocessOut'] ))
    print(self.BigStruct['CP_out'] )
    f1.write('CellprofOut: ' + str(self.BigStruct['CP_out'] ))
    f1.write('Parent: ' + str(self.BigStruct['Parent'] ))
    
    
    f1.write('Channels: ' + str(self.BigStruct['channels']) + '\n')
    f1.write('CPU_NUM: ' + str(self.BigStruct['CPU_NUM']) + '\n')
    f1.write('quiet: ' + str(self.BigStruct['quite']) + '\n')
    f1.write('ReOrg List: ' + str(self.BigStruct['ReOrgMatrix']) + '\n')
    
def openFiler(self,mode):
    if mode==1:
        fPathName,_ = QFileDialog.getOpenFileName(self, "Select Neural Net Model File", "/home/regotlab", "Keras/Tensorflow trained model (*.h5 *.hdf5)")
        self.model.setText(fPathName)
    if mode==2:
        fPathName,_ = QFileDialog.getOpenFileName(self, "Select CellProfiler Pipeline", "/home/regotlab","Cellprofiler (*.cppipe)")
        self.pipeline.setText(fPathName)



        
def openFileBrowser(self,buttonCode):
    
    dirPath = QFileDialog.getExistingDirectory(self, "Select Folder", "/home/regotlab")
    if len(dirPath) and buttonCode == "b1":
        self.ReOrg1.setText(dirPath)
    if len(dirPath) and buttonCode == "b2":
        self.ReOrg2.setText(dirPath)
    if len(dirPath) and buttonCode == "b3":
        self.ReOrg3.setText(dirPath)
    if len(dirPath) and buttonCode == "b4":
        self.ReOrg4.setText(dirPath)
    if len(dirPath) and buttonCode == "b5":
        self.ReOrg5.setText(dirPath)
    if len(dirPath) and buttonCode == "b6":
        self.Parent.setText(dirPath)        
    if len(dirPath) and buttonCode == "b7":
        self.prep_in.setText(dirPath)
    if len(dirPath) and buttonCode == "b8":
        self.CP_in.setText(dirPath)
    if len(dirPath) and buttonCode == "b9":
        self.tr_in.setText(dirPath)
    print(dirPath)
    print(self.ReOrg1.text())

def setter2(self):
    self.tabWidget.setCurrentWidget(self.Settings_Tab)
    
def setter1(self):
    self.tabWidget.setCurrentWidget(self.Input_Tab)

def StructUpdate(self):
    self.BigStruct['Flag'] = 0
    self.BigStruct['Particle'] = 1        
    self.BigStruct['testModeOn'] = self.radioButton_2.isChecked()
    self.BigStruct['reOrg'] = self.checkBox.isChecked()
    self.BigStruct['preprocess'] = self.checkBox_3.isChecked()
    self.BigStruct['cellprofiler'] = self.checkBox_2.isChecked()
    self.BigStruct['tracking'] = self.checkBox_4.isChecked()
    
    self.BigStruct['channels'] = []
    if len(self.c1.text()) > 0:
        self.BigStruct['channels'].append(self.c1.text())
    if len(self.c2.text()) > 0:
        self.BigStruct['channels'].append(self.c2.text())      
    if len(self.c3.text()) > 0:
        self.BigStruct['channels'].append(self.c3.text())
    if len(self.c4.text()) > 0:
        self.BigStruct['channels'].append(self.c4.text())
    if len(self.c5.text()) > 0:
        self.BigStruct['channels'].append(self.c5.text())
        
    self.BigStruct['CPU_NUM'] = self.spinBox_13.value()    
    self.BigStruct['quite'] = self.checkBox_14.isChecked()
    
    ReOrgCounter = 0    
    ReOrgMat = []
    if len(self.ReOrg1.text()) > 0:
        ReOrgCounter = ReOrgCounter + 1
        ReOrgMat1 = [self.ReOrg1.text(),self.Exp1.text(),self.FPR1.text(),self.FPW1.text(),self.FFR1.text(),self.FFW1.text(),self.LP1.text(),self.LI1.text()]
        ReOrgMat.append(ReOrgMat1)
    if len(self.ReOrg2.text()) > 0:
        ReOrgMat2 = [self.ReOrg2.text(),self.Exp2.text(),self.FPR2.text(),self.FPW2.text(),self.FFR2.text(),self.FFW2.text(),self.LP2.text(),self.LI2.text()]
        ReOrgCounter = ReOrgCounter + 1
        ReOrgMat.append(ReOrgMat2)
    if len(self.ReOrg3.text()) > 0:
        ReOrgMat3 = [self.ReOrg3.text(),self.Exp3.text(),self.FPR3.text(),self.FPW3.text(),self.FFR3.text(),self.FFW3.text(),self.LP3.text(),self.LI2.text()]
        ReOrgCounter = ReOrgCounter + 1
        ReOrgMat.append(ReOrgMat3)        
    if len(self.ReOrg4.text()) > 0:
        ReOrgMat4 = [self.ReOrg4.text(),self.Exp4.text(),self.FPR4.text(),self.FPW4.text(),self.FFR4.text(),self.FFW4.text(),self.LP4.text(),self.LI4.text()]
        ReOrgCounter = ReOrgCounter + 1
        ReOrgMat.append(ReOrgMat4)        
    if len(self.ReOrg5.text()) > 0:
        ReOrgMat5 = [self.ReOrg5.text(),self.Exp5.text(),self.FPR5.text(),self.FPW5.text(),self.FFR5.text(),self.FFW5.text(),self.LP5.text(),self.LI5.text()]
        ReOrgCounter = ReOrgCounter + 1
        ReOrgMat.append(ReOrgMat5)
   
    
    self.BigStruct['ReOrgCounter'] = ReOrgCounter
    self.BigStruct['ReOrgMatrix'] = ReOrgMat

    self.BigStruct['applyFlatFielding'] = self.checkBox_10.isChecked()
    self.BigStruct['applyImageRegistration'] = self.checkBox_11.isChecked()
    self.BigStruct['applyNeuralNetSegmentation'] = self.checkBox_12.isChecked()
    self.BigStruct['useSingleFrame'] = self.checkBox_13.isChecked()
    self.BigStruct['startFlatfieldPos'] = self.spinBox_2.value()
    self.BigStruct['endFlatfieldPos'] = self.spinBox.value()
    
    self.BigStruct['prefix'] = 'Pos'
    self.BigStruct['outputFilename'] = 'cpData.mat'
    self.BigStruct['processFrames'] = [] 
    self.BigStruct['subfolderNames'] = []  #Leave empty to process all
    self.BigStruct['frameFirstLast'] = []
   
    self.BigStruct['nuclearMarkerChannel'] = self.lineEdit_22.text() #name of nuc marker channel to segment with
    self.BigStruct['neuralNetModelPath'] = self.model.text() #filepath to keras .hdf5 model file
    self.BigStruct['cell_min_size'] = self.spinBox.value()
    self.BigStruct['saveNNProbMap'] = self.checkBox_6.isChecked() #will save raw pixel classification (boundary, background, foreground) in addition to mask creation
    self.BigStruct['useGPU'] = self.checkBox_5.isChecked()
    
    self.BigStruct['pipelineFilepath'] = self.pipeline.text()
    self.BigStruct['preClean'] = self.checkBox_7.isChecked()
    self.BigStruct['runCellProfiler'] = self.checkBox_8.isChecked()
    self.BigStruct['runChannelImageCompression'] = self.checkBox_9.isChecked()
    self.BigStruct['Parent'] = ""
    self.BigStruct['ReOrgOut'] = ""
    self.BigStruct['PreprocessOut'] = ""
    self.BigStruct['CP_out'] = ""
    
    trackParam = {}
    trackParam['maxdisp'] = [self.MaxDisp.value(),(self.MaxDisp.value()*0.8)] # The redius reduces by 0.95 and stops at 2
    trackParam['mem'] = self.MaxFrames.value()
    trackParam['good'] = self.MinLength.value()
    trackParam['dim'] = 2
    trackParam['quiet'] = self.BigStruct['quite']
    self.BigStruct['trackParam'] = trackParam
    self.BigStruct['outputSuffix'] = 'Tracked'
    
    if self.Parent.text():
        ParentPath = Path(self.Parent.text())
        self.BigStruct['Parent'] = str(ParentPath)
        self.BigStruct['ReOrgOut'] = str(ParentPath / 'RawImages')
        self.BigStruct['PreprocessOut'] = str(ParentPath / 'Images')
        self.BigStruct['CP_out'] = str(ParentPath / 'Output')
    
    if self.prep_in.text(): self.BigStruct['ReOrgOut'] = self.prep_in.text() # self.prep_in.text()    
    if self.CP_in.text(): self.BigStruct['PreprocessOut']  = self.CP_in.text()
    if self.tr_in.text(): self.BigStruct['CP_out'] = self.tr_in.text()
    
    self.BigStruct['objectSetNames'] = self.objectList.toPlainText().split(",")
    

def mainRunner(self):
    if self.BigStruct['testModeOn'] == False:
        if self.BigStruct['reOrg']:
            print('Running ReOrg')
            ReOrgStruct = {}
            ReOrgStruct['numCPU'] = self.BigStruct['CPU_NUM']
            ReOrgStruct['OF'] =  self.BigStruct['ReOrgOut']
            ReOrgStruct['Ch'] = self.BigStruct['channels'] 
            if self.BigStruct['ReOrgCounter']:
                for i in range(0,self.BigStruct['ReOrgCounter']):
                    ReOrgStruct['IP'] = self.BigStruct['ReOrgMatrix'][i][0]
                    ReOrgStruct['EP'] = self.BigStruct['ReOrgMatrix'][i][1] #Experiment Prefix"
                    ReOrgStruct['Image'] = (int(self.BigStruct['ReOrgMatrix'][i][4]),int(self.BigStruct['ReOrgMatrix'][i][5])) #(x,y), first image number to read and first to write. Default is 1,0
                    ReOrgStruct['Position'] = (int(self.BigStruct['ReOrgMatrix'][i][2]),int(self.BigStruct['ReOrgMatrix'][i][3])) #(x,y), first position number to read and first to write. Default is 1,0
                    ReOrgStruct['LastImg'] = int(self.BigStruct['ReOrgMatrix'][i][7]) #will default to final frame of ExpPrefix.
                    ReOrgStruct['LastPos'] = int(self.BigStruct['ReOrgMatrix'][i][6]) #will default to final position of ExpPrefix.
                    ReOrgMetFull(ReOrgStruct)
            print('ReOrg succesful')
        if self.BigStruct['preprocess']:
            preprocessingStruct = {}
            print('Running preprocessing')
            preprocessingStruct['quite'] = self.BigStruct['quite']
            preprocessingStruct['inputParentPath'] = self.BigStruct['ReOrgOut']
            preprocessingStruct['outputParentPath'] = self.BigStruct['PreprocessOut']
            preprocessingStruct['CPU_NUMs'] = self.BigStruct['CPU_NUM']
            preprocessingStruct['channels'] = self.BigStruct['channels'] 
            preprocessingStruct['applyImageRegistration'] = self.BigStruct['applyImageRegistration']
            preprocessingStruct['applyNeuralNetSegmentation']  = self.BigStruct['applyNeuralNetSegmentation'] 
            preprocessingStruct['applyFlatFielding'] = self.BigStruct['applyFlatFielding']
            preprocessingStruct['UseSingleFrame'] = self.BigStruct['useSingleFrame'] 
            preprocessingStruct['applyImageRegistration'] = self.BigStruct['applyImageRegistration']
            preprocessingStruct['applyNeuralNetSegmentation'] = self.BigStruct['applyImageRegistration']
            preprocessingStruct['prefix'] = self.BigStruct['prefix'] 
            preprocessingStruct['processFrames'] = self.BigStruct['processFrames'] 
            preprocessingStruct['subfolderNames'] =  self.BigStruct['subfolderNames']
            preprocessingStruct['nuclearMarkerChannel'] = self.BigStruct['nuclearMarkerChannel'] 
            preprocessingStruct['neuralNetModelPath'] =  self.BigStruct['neuralNetModelPath']
            preprocessingStruct['cell_min_size'] = self.BigStruct['cell_min_size']
            preprocessingStruct['saveNNProbMap'] = self.BigStruct['saveNNProbMap'] 
            preprocessingStruct['useGPU'] = self.BigStruct['useGPU'] 
            #print(preprocessingStruct['useGPU'] )
            preprocessImagesCaller(preprocessingStruct)
            print('preprocess complete')    
        if self.BigStruct['cellprofiler']:
            print('Running CellProfiler')
            analyzeParentDirCp(self.BigStruct['pipelineFilepath'],  self.BigStruct['PreprocessOut'],  self.BigStruct['CP_out'],
                self.BigStruct['outputFilename'], self.BigStruct['subfolderNames'], self.BigStruct['frameFirstLast'], 'cellprofiler',
                self.BigStruct['preClean'], self.BigStruct['runCellProfiler'], self.BigStruct['runChannelImageCompression'], self.BigStruct['CPU_NUM'])
        if self.BigStruct['tracking']:
            print('Running Tracking')        
            trackStruct = {}
            trackStruct['parentPath'] = self.BigStruct['CP_out']
            trackStruct['cpDataFilename'] = self.BigStruct['outputFilename']
            trackStruct['objectSetNames'] = self.BigStruct['objectSetNames']
            trackStruct['subfolderNames'] = self.BigStruct['subfolderNames'] 
            trackStruct['trackParam'] = self.BigStruct['trackParam'] 
            trackStruct['outputSuffix'] = self.BigStruct['outputSuffix']

            trackOrganizeCpDataDir(trackStruct)
            print('Tracking Complete!')

def checkybox(self):
    print('plz')
    if self.checkBox.isChecked:
        self.Channels.setEnabled(True)
 
def test1():
    print('1')

def test2(Struct1):
    print(Struct1['ReOrgCounter'])
    print(Struct1)

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()