import sys,os
from images import qpicture
from PyQt5.QtWidgets import QMainWindow,QApplication,QColorDialog,QPushButton,QDialog,QFileDialog,QLabel,QDesktopWidget,QWidget
from PyQt5.QtGui import QPixmap,QPicture
from PyQt5.QtCore import Qt,QTime,QTimer
from PyQt5.uic import loadUiType
from PyQt5.QtMultimedia import QSound


nowdir=sys.argv[0].replace(r'\testsheet.py','')
os.chdir(nowdir)
qtCreatorFile = r'UI\mainwindow.ui'     #导入第一个窗口
Ui_MainWindow,QtBaseClass = loadUiType(qtCreatorFile)
qtCreatorFile1 = r'UI\fullscreen.ui'      #导入第二个窗口
Ui_FullScreen,QtBaseClass1 = loadUiType(qtCreatorFile1)

class test (QDialog,Ui_FullScreen,QLabel):
    def __init__(self):
        QDialog.__init__(self)
        Ui_FullScreen.__init__(self)
        self.setupUi(self)
        
    
    def setUI(self):
        self.label=QLabel('',self)
        size=QDesktopWidget().screenGeometry()
        self.label.setGeometry(0,0,size.width(),size.height())
        print (self.view_leftup.size())        
        pixMap = QPixmap(r'picture\blackblock.png').scaled(self.label.width(),self.label.height())
        self.label.setPixmap(pixMap)  
        self.label.lower()    
        
        
        
         
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    window = test()
    window.showFullScreen()
    window.setUI()
    sys.exit(app.exec_())