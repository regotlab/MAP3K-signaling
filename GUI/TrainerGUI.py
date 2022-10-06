import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from datetime import datetime
from pathlib import Path
import subprocess
import numpy as np
import skimage.io as skio
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


from trainGUI import Ui_MainWindow

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
        self.imCounter = 0
        self.ImList = []
        self.MaskList = []
        self.b1.clicked.connect(lambda: openFileBrowser(self,1))
        self.ParentDir.textChanged.connect(lambda: dirUpdater(self,1))
        self.b1.clicked.connect(lambda: dirUpdater(self,1))
        self.b3.clicked.connect(lambda: openFiler(self,1))
        self.b4.clicked.connect(lambda: saver(self,1))
        self.Example.clicked.connect(lambda: dirUpdater(self,1))
        self.Example.clicked.connect(lambda: imLister(self))
        self.Example.clicked.connect(lambda: imageLoader(self,1))
        self.Annotate.clicked.connect(lambda: imLister(self))
        self.Annotate.clicked.connect(lambda: annotator(self))
        
        self.Eval.clicked.connect(lambda: setEvaluate(self))
        
        self.ASettings.clicked.connect(lambda: setAdvanced(self))

        self.layout
        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        #self.imLabel.layout().addWidget(static_canvas)
        self.addToolBar(NavigationToolbar(static_canvas, self))
        self.L1_Mask.layout().addWidget(static_canvas)
        
        s_canvas_2 = FigureCanvas(Figure(figsize=(5,3)))
        self.L1_Label.layout().addWidget(s_canvas_2)

        ax1, ax2 = static_canvas.figure.subplots(1,2,sharex=True,sharey=True)
        static_canvas.figure.subplots_adjust(left=0, right=.98, top=.98, bottom=0.1)
        t = np.linspace(0, 10, 501)
        print(ax1)
        print(ax2)
        ax1.plot(t, np.tan(t), ".")
        ax2.plot(t, np.cos(t),".")
        
        ax3 = s_canvas_2.figure.subplots(1,1,sharex=True,sharey=True)
        
        ax3.get_shared_x_axes().join(ax3,ax2)
        ax3.get_shared_y_axes().join(ax3,ax2)
        

        #s_canvas_2.figure.axis('off')
        ax2.axis('off')
        ax1.axis('off')
        ax3.axis('off')
        
        self.setWindowTitle('wooo')
        
        
def setEvaluate(self):
    self.tabWidget.setCurrentWidget(self.Evaluate)

def setAdvanced(self):
    self.tabWidget.setCurrentWidget(self.Advanced)


        
def imLister(self):
    print(self.ImDir)
    imDir = Path(self.ImDir)
    maskDir = Path(self.MaskDir)
    igen = sorted(imDir.glob('*png'))
    igen2 = sorted(imDir.glob('*tif'))
    ilist = igen
    if igen2: ilist.append(igen2)
    mgen = sorted(maskDir.glob('*png'))
    mgen2 = sorted(maskDir.glob('*tif'))
    mlist = mgen
    if mgen2: mlist.append(mgen2)
    self.ImList = ilist
    self.MaskList = mlist
    
def annotator(self):
    import os
    os.path.isfile('caliban/desktop/caliban.py')
    os.path.exists('caliban')
    fz = '/home/regotlab/Documents/TrainingData/HEK293/HEK293.npz'
    im1 = skio.imread(str(self.ImList[0]))
    lx = len(self.ImList)
    a = im1.shape
    b = (lx,a[0],a[1],1)
    X = np.empty(b)
    y = X
    for i in range(0,lx):
        fname = str(self.ImList[i])
        X[i,:,:,0] = skio.imread(fname)
        y[i,:,:,0] = skio.imread(str(self.MaskList[i]))[:,:,0]
    outfn = str( Path(self.ParentDir.text()) / 'training.npz')
    np.savez(outfn,X,y)
        
    L1 = ['python', 'caliban/desktop/caliban.py',outfn]
    subprocess.call(L1)
    
def dirUpdater(self,mode):
    if self.ParentDir.text() and mode == 1:
        self.ImDir = str((Path(self.ParentDir.text()) / 'Images'))
        self.MaskDir = str((Path(self.ParentDir.text()) / 'Masks'))
        
def openFileBrowser(self,buttonCode):
    
    dirPath = QFileDialog.getExistingDirectory(self, "Select Parent Folder", "/home/regotlab")
    print(dirPath)
    if dirPath and buttonCode == 1:
        self.ParentDir.setText(dirPath)
        self.ImList = []
        
def openFiler(self,mode):
    fPathName,_ = QFileDialog.getOpenFileName(self, "Select Neural Net Model File", "/home/regotlab", "Keras/Tensorflow trained model (*.h5 *.hdf5)")
    if fPathName and mode==1:
        self.OldModel.setText(fPathName)

def saver(self,mode):
    if mode==1:
        saveName,_ = QFileDialog.getSaveFileName(self, "Save model as", "/home/regotlab","Keras/Tensorflow trained model (*.h5 *.hdf5)")
        self.SaveModel.setText(saveName)

def imageLoader(self,mode):
    if mode == 1:
        c = self.imCounter
        pmapIm = QPixmap(str(self.ImList[c]))
        print(str(self.MaskList[c]))
        print(self.MaskList)
        pmapL = QPixmap(str(self.MaskList[c]))
        pmapIm2 = pmapIm.scaled(291, 211, Qt.KeepAspectRatio)
        pmapL2 = pmapL.scaled(291, 211, Qt.KeepAspectRatio)
        self.imImage.setPixmap(pmapIm2)
        self.imMask.setPixmap(pmapL2)
        self.imCounter = self.imCounter + 1

        
    
    

app = QtWidgets.QApplication(sys.argv)
        
window = MainWindow()
window.show()
app.exec()