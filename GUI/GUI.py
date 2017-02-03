import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):
    #init is the first thing that runs
    def __init__(self):
        super(Window,self).__init__() 
        self.setGeometry(50,50,500,300)
        self.setWindowTitle("Drone")
        self.setWindowIcon(QtGui.QIcon('smu.png'))

        extractAction = QtGui.QAction("&Leave",self)
        extractAction.setShortcut("Ctrl+Q") #Shortcut to exit the GUI
        extractAction.setStatusTip('Leave the app')
        extractAction.triggered.connect(self.close_application)
        extractAction1 = QtGui.QAction("&Solve",self)
        extractAction1.setShortcut("Ctrl+S")
        extractAction1.setStatusTip('Solve for q')
        extractAction1.triggered.connect(self.counter)
        
        self.statusBar()
        
        mainMenu = self.menuBar() #assigned to variable because needs to be modified
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        openMenu = mainMenu.addMenu('&Open')
        openMenu.addAction(extractAction1)
        
        self.home()
        
      
    def home(self):
        btn = QtGui.QPushButton("Quit",self) #Quit button
        btn.clicked.connect(self.close_application) #argument is Qt built in quit
        btn.resize(btn.sizeHint()) #Let Qt decide the size
        btn.move(400,250)
        btn1 = QtGui.QPushButton("Start",self)
        btn1.resize(btn1.sizeHint())
        btn1.move(50,250)

        #extractAction = QtGui.QAction(QtGui.QIcon('smu.png'),'Test',self)
        #extractAction.triggered.connect(self.close_application)

        #self.toolBar = self.addToolbar("Extraction")
        #self.toolBar.addAction(extractAction)
        
        self.show()
    def close_application(self):
         for y in range(0, 20):
            print ("The new number is: ",y)
            if y == 19:
                sys.exit()
    def counter(self):
            x = 4*3
            z = 149
            q = x-z
            print(q)
    
        
    
        
#run is the main loop
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
