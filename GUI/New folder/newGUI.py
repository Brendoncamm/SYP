import sys
from PyQt5 import QtWidgets, QtGui, QtCore



class GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(GUI,self).__init__()
        self.title = 'Drone'
        self.setGeometry(50,50,500,300)
        self.setWindowTitle("Drone")
        self.setWindowIcon(QtGui.QIcon('smu.png'))
        self.home()

    def home(self):
        btn = QtWidgets.QPushButton("Quit",self)
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        btn.resize(100,25)
        btn.move(0,275)
        hbox = QtWidgets.QVBoxLayout()
        self.setLayout(hbox)
        hbox.addWidget(btn)
        self.show()

 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = GUI()
    main.show()
    sys.exit(app.exec_())
