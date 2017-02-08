import sys, os.path
import callscript
from PyQt4 import QtCore, QtGui, uic

qtCreatorFile = "GUI.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)



class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Drone")
        self.setWindowIcon(QtGui.QIcon('smu.png'))
        self.pushButton_2.clicked.connect(self.close_application)
        self.pushButton.clicked.connect(self.addition)
        self.color_change()
    def addition(self):
        num1 = int(input("enter number: "))
        num2 = int(input("enter number: "))
        ans = callscript.addition(num1,num2)
        self.text.setText(ans)
        return ans
    def close_application(self):
        sys.exit()
    def color_change(self):
        if os.path.exists('/Users/Brendon/Desktop/ECED4900/SYP/GUI/callscript.py'):
            self.label.setStyleSheet('QLabel { color: green }')
        else:
            self.label.setStyleSheet('QLabel { color: Red }')
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    
