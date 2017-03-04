import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolBar)
from matplotlib.figure import Figure
import numpy as np
import time
import struct
import socket
from PS4_Controller import PS4Controller as PS4

qtCreatorFile = "GUI.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)



class GUI(QtWidgets.QMainWindow, Ui_MainWindow, QtWidgets.QMenu,):   #Inherit PS4 eventually
    def __init__(self):

        #Qt initialization
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.page = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.page)
        self.setupUi(self)
        self.setWindowTitle("Drone")
        self.setWindowIcon(QtGui.QIcon('smu.png'))

        #Networking
        getHost = socket.gethostname()
        #Main Page buttons
        self.start.clicked.connect(self.connection)
        self.end.clicked.connect(self.stop)

        #Listing widget
        self.list.insertItem(0, 'Home')
        self.list.insertItem(1, 'Controller')
        self.list.insertItem(2, 'Distance') 
        self.list.currentRowChanged.connect(self.display)

        #Controller Page
        self.axisVal.setText('1 2 3 4')
        self.hostVal.setText(getHost)
        self.portVal.setText('2222')
        self.axisMenu.clicked.connect(self.axisSettings)
        self.hostMenu.clicked.connect(self.hostSettings)
        self.portMenu.clicked.connect(self.portSettings)
        self.updateConnect.clicked.connect(self.updateConnection)
    def stop(self):
        sys.exit(app.exec_())
    def connection(self):
        s = socket.socket()
        host = socket.gethostbyname('Brendon-PC')
        port = 1247
        status = s.connect_ex((host,port)) #Returns 0 if true
        if status: # Status = errno
            self.thisworks.setText("Connection Unsuccessful")
        else: # Status = 0
            print(status)
            self.thisworks.setText("Connection Successful")
            
    def addmpl(self,fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolBar = NavigationToolBar(self.canvas,
                                         self.windowmpl,
                                         coordinates = True)
        self.mplvl.addWidget(self.toolBar)
  
    def axisSettings(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Input', ' Type text:')
        t = str(text)
        if t == '':
            self.axisVal.setText('1 2 3 4')
        else:
            self.axisVal.setText(t)
    def display(self,i):
        self.home.setCurrentIndex(i)
    def addData(self,name,fig):
        self.fig_duct[name] = fig
        self.list.addItem(name)
    def hostSettings(self):
        text, ok = QtWidgets.QInputDialog.getText(self,'Input', 'Type text:')
        newHost = str(text)
        if newHost == '':
            self.hostVal.setText(socket.gethostname())
        else:
            self.hostVal.setText(newHost)
        return newHost
    def portSettings(self):
        text, ok = QtWidgets.QInputDialog.getText(self,'Input','Type text:')
        newPort = str(text)
        if newPort == '':
            self.portVal.setText('2222')
        else:
            self.portVal.setText(newPort)
        return int(newPort)
    def updateConnection(self):
        host1 = self.hostSettings()
        port1 = self.portSettings()
        s = socket.socket()
        status = s.connect_ex((host1,port1))
        if status:
            self.connectionStat.setText("Update and Connection Unsuccessful")
            #socket.send('Success')
        else:
            self.connectionStat.setText("Update and connection Successful")
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
    

   
    
