import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolBar)
from matplotlib.figure import Figure
import numpy as np
import time
from timeit import default_timer as timer
import struct
import socket
from dictionaryTest import a

qtCreatorFile = "GUI.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)



class GUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
       
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.page = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.page)
        self.setupUi(self)
        self.setWindowTitle("Drone")
        self.setWindowIcon(QtGui.QIcon('smu.png'))
        self.start.clicked.connect(self.connection)
        self.end.clicked.connect(self.stop)
        self.list.insertItem(0, 'Home')
        self.list.insertItem(1, 'Controller')
        self.list.insertItem(2, 'Notes')
        self.list.insertItem(3, 'New Plot')
        self.list.currentRowChanged.connect(self.display)
    def stop(self):
        sys.exit(app.exec_())
    def connection(self):
        s = socket.socket()
        host = socket.gethostbyname('Brendon-PC') #Will change to RPI eventually
        port = 1247
        s.connect((host,port))
        status = s.connect_ex((host,port))
        s.close()
        if status:
            self.thisworks.setText("Connection Successful")
        else:
            self.thisworks.setText("Connection unsuccessful")
            
            
    def addmpl(self,fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolBar = NavigationToolBar(self.canvas,
                                         self.windowmpl,
                                         coordinates = True)
        self.mplvl.addWidget(self.toolBar)
  
    def Controller(self):
        layout = QFormLayout()
        self.Controller.setLayout(layout)
    def Notes(self):
        layout = QFormLayout()
        self.Notes.setLayout(layout)
    def NotSure(self):
        layout = QFormLayout()
        self.NoteSure.setLayout(layout)
    def display(self,i):
        self.home.setCurrentIndex(i)

    
if __name__ == '__main__':
    x1 = np.linspace(0.0,5.0)
    y1 = np.cos(2*np.pi*x1)
    fig1 = Figure()
    axlfl = fig1.add_subplot(111)
    axlfl.plot(x1,y1)
    app = QtWidgets.QApplication(sys.argv)
    main = GUI()
    main.addmpl(fig1)
    main.show()
    sys.exit(app.exec_())
    

   
    
