import sys, os.path
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import time
from timeit import default_timer as timer
qtCreatorFile = "GUI.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)



class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
      
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Drone")
        self.setWindowIcon(QtGui.QIcon('smu.png'))
        self.start.clicked.connect(self.timeStart)
        self.end.clicked.connect(self.stop)
    def timeStart(self):
        start = timer()
        while start<100:
            end = timer()
            time.sleep(1)
            print(end-start)
            
    def stop(self):
        sys.exit(app.exec_())
    def addmpl(self,fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        
if __name__ == '__main__':
    fig1 = Figure()
    axlfl = fig1.add_subplot(111)
    axlfl.plot(np.random.rand(5))
    app = QtWidgets.QApplication(sys.argv)
    main = MyApp()
    main.addmpl(fig1)
    main.show()
    sys.exit(app.exec_())
    

   
    
