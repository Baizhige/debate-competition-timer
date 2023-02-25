import sys
import re
from PyQt5.QtWidgets import QMainWindow,QApplication,QColorDialog,QPushButton,QDialog,QFileDialog,QLabel,QDesktopWidget
#from PyQt5.QtGui import *
from PyQt5.QtCore import Qt,QTime,QTimer
from PyQt5.uic import loadUiType
from PyQt5.QtMultimedia import QSound
import xlrd
qtCreatorFile = r'C:\Users\Eloit\Desktop\GUIforDebate\UI\mainwindow.ui'     #导入第一个窗口
Ui_MainWindow,QtBaseClass = loadUiType(qtCreatorFile)
qtCreatorFile1 = r'C:\Users\Eloit\Desktop\GUIforDebate\UI\fullscreen.ui'    #导入第二个窗口
Ui_FullScreen,QtBaseClass1 = loadUiType(qtCreatorFile1)


#---global-var--------------------------------------
competition_rules=[]             #赛制
page=0                           #环节
Var_Zname ,Var_Fname,Var_Zviewpoint,Var_Fviewpoint = '','','',''       #基础名字
#samplelist=[]
#---global-var-----------------------------------------

def QTimeStrToInt(str):               #自定义函数：将QTime类的Qstring 返回成秒
    str+='0'
    
    min=int(str[:2])
    sec=int(str[3:5])
   
    result = min*60+sec

    return result


class FullScreen(QDialog,Ui_FullScreen):  
    def __init__(self):
        QDialog.__init__(self)
        Ui_FullScreen.__init__(self)
        self.setupUi(self)
        self.slots()                      #等待所有信号
        self.sound_zero=QSound(r'C:\Users\Eloit\Desktop\GUIforDebate\voice\dianzibaojing.wav')             #载入音频文件
        #------widgets-init--------------------
        self.labelcenter=QLabel('',self)               #中央提示文本的label
        self.widgetscenter(self.labelcenter)
        self.labelcenter.show()
        #------widgets-init--------------------
    #-------slots--------------
    def go(self):            #环节向前
        global page
        self.sound_zero.stop()
        page+=1
        self.fullscreenUI()
        
    def back(self):          #环节退后
        global page
        self.sound_zero.stop()
        page-=1
        self.fullscreenUI()
    def lefttip(self):      #提醒按键
        if competition_rules[page][10]!='N':
            self.labelcenter.setText(competition_rules[page][10])
        
    def righttip(self):     #提醒按键
        if competition_rules[page][11]!='N':
            self.labelcenter.setText(competition_rules[page][11])
    
    def update(self):      #每秒执行一次的槽函数   （核心）
        if self.bool_isstart and (self.bool_btn_left or self.bool_left):  #总的开关：是否流逝
            if self.ZAllTime.toString('mm:ss')!='00:00':  #对正方所有时间的操作
                self.ZAllTime=self.ZAllTime.addSecs(-1)
            else:
                self.sound_zero.play()
            
        if self.bool_btn_left:                             #判断正方是否在讲话
            if self.ZOnceTime.toString('mm:ss')!='00:00':  #对正方单次时间的操作
                self.ZOnceTime=self.ZOnceTime.addSecs(-1)
            else:                
                self.sound_zero.play()
            self.lcd_center.display(self.ZOnceTime.toString('mm:ss'))      #显示
        self.lcd_left.display(self.ZAllTime.toString('mm:ss'))     #显示所有
        
                
        if self.bool_isstart and (self.bool_btn_right or self.bool_right):  #总的开关：是否流逝
            if self.FAllTime.toString('mm:ss')!='00:00':
                self.FAllTime=self.FAllTime.addSecs(-1)
            else:
                self.sound_zero.play()
        if self.bool_btn_right:
                
            if self.FOnceTime.toString('mm:ss')!='00:00':
                self.FOnceTime=self.FOnceTime.addSecs(-1)
            else:
                self.sound_zero.play()
            self.lcd_center.display(self.FOnceTime.toString('mm:ss'))
        self.lcd_right.display(self.FAllTime.toString('mm:ss'))
        

    def btnleftclick(self):       #正方按钮的效果
        
        if self.bool_btn_left:
            pass
                    
        else:
            if self.bool_isstart==False:
                self.bool_isstart=True
            self.sound_zero.stop()
            self.ZOnceTime=QTime(0,0,0)
            if self.Var_ZOnceTime <= QTimeStrToInt(self.ZAllTime.toString('mm:ss')):
                self.ZOnceTime=self.ZOnceTime.addSecs(self.Var_ZOnceTime)
            else:
                self.ZOnceTime=self.ZOnceTime.addSecs(QTimeStrToInt(self.ZAllTime.toString('mm:ss')))
            self.bool_btn_left=True
            self.bool_btn_right=False
            
            
            
    def btnrightclick(self):
         if self.bool_btn_right:
            pass
                    
         else:
            if self.bool_isstart==False:
                self.bool_isstart=True
            self.sound_zero.stop()
            self.FOnceTime=QTime(0,0,0)
            if self.Var_FOnceTime <= QTimeStrToInt(self.FAllTime.toString('mm:ss')):
                self.FOnceTime=self.FOnceTime.addSecs(self.Var_FOnceTime)
            else:
                self.FOnceTime=self.FOnceTime.addSecs(QTimeStrToInt(self.FAllTime.toString('mm:ss')))
            self.bool_btn_right=True
            self.bool_btn_left=False
            
            
         
         
                
    #-------slots--------------     #槽函数结束  
    
    def slots(self):      
        self.btn_back.clicked.connect(self.back)
        self.btn_go.clicked.connect(self.go)
    
        
    def keyPressEvent(self,e):#16777216
        if e.key() == 16777216:
            self.close()
    
    def widgetscenter(self,widgets):
        screen = QDesktopWidget().screenGeometry()
        size = widgets.geometry()
        widgets.move((screen.width() - size.width()) /2,(screen.height() - size.height())/2)
        
            
    
    def fullscreenUI(self):
        #-----button----
        
        if competition_rules[page][2] =='N':
            self.btn_left.setVisible(False)
        else:
            self.btn_left.setVisible(True)
        if competition_rules[page][3] =='N':
            self.btn_right.setVisible(False)
        else:
            self.btn_right.setVisible(True)
        if page == 0:
            self.btn_back.setVisible(False)
        else:
            self.btn_back.setVisible(True)
        if page == (len(competition_rules)-1):
            self.btn_go.setVisible(False)
        else:
            self.btn_go.setVisible(True)
        if competition_rules[page][10]:
            self.btn_left.clicked.connect(self.lefttip)
        if competition_rules[page][11]:
            self.btn_right.clicked.connect(self.righttip)
            
        #-----button----
        
        #-----label-----
        
        self.labelcenter.setText('')
        if competition_rules[page][2]!='N':
            self.lab_left.setText(competition_rules[page][2])
        else:
            self.lab_left.setText('')
        if competition_rules[page][3]!='N':
            self.lab_right.setText(competition_rules[page][3])
        else:
            self.lab_right.setText('')
            
        self.lab_leftup2.setText(Var_Zname)
        self.lab_leftup3.setText(Var_Zviewpoint)
        self.lab_rightup2.setText(Var_Fname)
        self.lab_rightup3.setText(Var_Fviewpoint)
        self.lab_centerup.setText(competition_rules[page][1])
        self.lab_center.setText(competition_rules[page][1])
        #-----label-----
        
        #-----lcdnumber-----
        
        
        if competition_rules[page][2] == 'N':
            self.lcd_left.setVisible(False)
        else:
            self.lcd_left.setVisible(True)
        
        if competition_rules[page][3] == 'N':
            self.lcd_right.setVisible(False)
        else:
            self.lcd_right.setVisible(True)
        
        if competition_rules[page][5] == 'N':
            pass
        else:
            
            self.Var_ZAllTime=int(competition_rules[page][6])
            self.Var_FAllTime=int(competition_rules[page][7])
            self.Var_ZOnceTime=int(competition_rules[page][8])
            self.Var_FOnceTime=int(competition_rules[page][9])
            
            
            self.bool_btn_left=False
            self.bool_btn_right=False
            self.bool_isstart=False
            if competition_rules[page][12]:
                self.bool_left=True   #is can't control
            else:
                self.bool_left=False 
            
            if competition_rules[page][13]:
                self.bool_right=True
            else:
                self.bool_right=False
            
            
            self.timer=QTimer()
            
            self.ZOnceTime=QTime(0,0,0)
            self.FOnceTime=QTime(0,0,0)
            self.ZAllTime=QTime(0,0,0)
            self.FAllTime=QTime(0,0,0)
            self.ZOnceTime=self.ZOnceTime.addSecs(self.Var_ZOnceTime)
            self.FOnceTime=self.FOnceTime.addSecs(self.Var_FOnceTime)
            self.ZAllTime=self.ZAllTime.addSecs(self.Var_ZAllTime)
            self.FAllTime=self.FAllTime.addSecs(self.Var_FAllTime)    
            self.lcd_left.display(self.ZAllTime.toString('mm:ss'))
            self.lcd_right.display(self.FAllTime.toString('mm:ss'))
            self.lcd_center.display('00:00')            
            ###########
            self.btn_right.clicked.connect(self.btnrightclick)
            self.btn_left.clicked.connect(self.btnleftclick)
            self.timer.timeout.connect(self.update)
            self.timer.start(1000)  
        #-----lcdnumber-----
        
        
        
class MyApp(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.signal()    
    def signal (self):
        self.pg1_btn_enter.clicked.connect(self.enter)
        self.pg2_tbtn_filechoose.clicked.connect(self.filechoose)
        self.pg3_tbtn_01.clicked.connect(self.waitingmusicfile)
        self.pg3_tbtn_02.clicked.connect(self.medalmusicfile)
        self.pg3_tbtn_11.clicked.connect(self.timesupvociefile)
        self.pg3_tbtn_21.clicked.connect(self.warnningvociefile)
        self.pg3_tbtn_31.clicked.connect(self.didavociefile)
        self.pg3_tbtn_41.clicked.connect(self.oncespeaktimesupvociefile)
        self.pg4_btn_02.clicked.connect(self.backgroundfile)
        self.pg4_btn_01.clicked.connect(self.showDialog1)
        self.pg4_btn_11.clicked.connect(self.showDialog2)
        self.pg4_btn_12.clicked.connect(self.medalfile)
        self.pg4_btn_21.clicked.connect(self.camp1show)
        self.pg4_btn_22.clicked.connect(self.camp2show)
        self.pg4_btn_31.clicked.connect(self.startpicfile)
        #####
        self.pg4_rbtn_01.clicked.connect(self.pg4updatebutton)
        self.pg4_rbtn_02.clicked.connect(self.pg4updatebutton)
        self.pg4_rbtn_03.clicked.connect(self.pg4updatebutton)
        self.pg4_rbtn_11.clicked.connect(self.pg4updatebutton)
        self.pg4_rbtn_12.clicked.connect(self.pg4updatebutton)
        self.pg4_rbtn_13.clicked.connect(self.pg4updatebutton)
        #####
        
        
        
    #-----------THIS-IS-SLOTS---------------------------
    def enter (self):
        
        '''
        global samplelict
        checklist=[]
        for x in competition_rules:
            if x[0] in checklist:
                samplelict.append(x[0])
            else:
                checklist.append(x[0])
        print (samplelist)
        '''
       
        fullscreenrun()
        
    def filechoose(self): 
        global competition_rules
        fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取赛制文件",  "C:/",  "Text Files (*.xlsx)")
        if fileName1 :
            f=xlrd.open_workbook(r'D:\计时器\电子计时器\guangzhou competition rules.xlsx')
            sheets=f.sheets()
            sheet=sheets[0]
            n=1
            L_all=[]
        # 读取 一个L表示一个环节，一个competition_rules的list表示所有环节
            while sheet.cell_value(n, 0) != 0.0:
                i=0
                L=[]
                while i != 14:
                    value = sheet.cell_value(n, i)
                    L.append(value)
                    i+=1
                L_all.append(L)
                n+=1
            competition_rules = L_all    
            #print (competition_rules)
        else:
            print ('没有读取到xlsx文件')        
    
    def waitingmusicfile(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取文件",  "C:/",  "All Files (*);;Text Files (*.txt)")
        
    
    def medalmusicfile(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取文件",  "C:/",  "All Files (*);;Text Files (*.txt)")
        
    
    def timesupvociefile(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取文件",  "C:/",  "All Files (*);;Text Files (*.txt)")
        
    
    def warnningvociefile(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取文件",  "C:/",  "All Files (*);;Text Files (*.txt)")
        
    
    def didavociefile(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取文件",  "C:/",  "All Files (*);;Text Files (*.txt)")
        
        
    def oncespeaktimesupvociefile(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取文件",  "C:/",  "All Files (*);;Text Files (*.txt)")
        
    def showDialog1(self):
      
        col = QColorDialog.getColor()

    def backgroundfile(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取文件",  "C:/",  "All Files (*);;Text Files (*.txt)")
        
    def showDialog2(self):
      
        col = QColorDialog.getColor()
     
    def medalfile(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取文件",  "C:/",  "All Files (*);;Text Files (*.txt)")
    
    def camp1show(self):
        pass
    
    def camp2show(self):
        pass
    
    def startpicfile (self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取文件",  "C:/",  "All Files (*);;Text Files (*.txt)")
    
    def pg4updatebutton(self):
        
        if self.pg4_rbtn_02.isChecked():
            self.pg4_btn_01.setEnabled(True)
        else:
            self.pg4_btn_01.setEnabled(False)
        
        if self.pg4_rbtn_03.isChecked():
            self.pg4_btn_02.setEnabled(True)
        else:
            self.pg4_btn_02.setEnabled(False)
            
        if self.pg4_rbtn_12.isChecked():
            self.pg4_btn_11.setEnabled(True)
        else:
            self.pg4_btn_11.setEnabled(False)
            
        if self.pg4_rbtn_13.isChecked():
            self.pg4_btn_12.setEnabled(True)
        else:
            self.pg4_btn_12.setEnabled(False)
    #-----------THIS-IS-SLOTS---------------------------
            
            
            
            
def competition_rules_translate(x):
     Vardict=globals()
     
     if isinstance(x,str) and re.match(r'^Var_[0-9a-zA-Z\_]+$',x) and x in Vardict:
         return Vardict[x]
     else:
         return x
                  
            
def fullscreenrun ():
    global Var_Zname ,Var_Fname,Var_Zviewpoint,Var_Fviewpoint,competition_rules
    Var_Zname = window.pg1_lineEdit_1.displayText()    
    Var_Fname = window.pg1_lineEdit_2.displayText()
    Var_Zviewpoint = window.pg1_lineEdit_4.displayText()
    Var_Fviewpoint = window.pg1_lineEdit_4.displayText()
    for i in range(0,len(competition_rules)):
        competition_rules[i]=list (map(competition_rules_translate,competition_rules[i]))
        window1.fullscreenUI()

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window1 = FullScreen()
    window.pg1_btn_enter.clicked.connect(window1.showFullScreen)
    window.show()
    sys.exit(app.exec_())
    
