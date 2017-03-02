from PyQt5 import QtGui, QtWidgets,QtCore,uic
from PyQt5.uic import loadUiType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import numpy as np

qtCreatorFile = "GUI.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType('GUI.ui')

class Main(QtWidgets.QMainWindow, Ui_MainWindow):
  def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        fig1 = Figure()
        axlfl = fig1.add_subplot(111)
        axlfl.plot(np.random.rand(5))

        
  def addmpl(self,fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
if __name__ == '___main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())



                
                

