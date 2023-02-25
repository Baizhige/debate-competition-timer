import sys,os
import re
from PyQt5.QtWidgets import QMainWindow,QApplication,QColorDialog,QPushButton,QDialog,QFileDialog,QLabel,QDesktopWidget,QWidget
from PyQt5.QtGui import QPixmap,QBrush,QPalette,QIcon
from PyQt5.QtCore import Qt,QTime,QTimer
from PyQt5.uic import loadUiType
from PyQt5.QtMultimedia import QSound
from images import qpicture
import xlrd
nowdir=sys.argv[0].replace(r'\GUI PyQt.py','')
os.chdir(nowdir)
qtCreatorFile = r'UI\mainwindow.ui'     #导入第一个窗口
Ui_MainWindow,QtBaseClass = loadUiType(qtCreatorFile)
qtCreatorFile1 = r'UI\fullscreen.ui'      #导入第二个窗口
Ui_FullScreen,QtBaseClass1 = loadUiType(qtCreatorFile1)


#---global-var--------------------------------------
competition_rules=[]             #赛制
page=0                           #环节
Var_Zname ,Var_Fname,Var_Zviewpoint,Var_Fviewpoint = '','','',''       #基础名字
File_OnceTimesup,File_AllTimesup,File_WarnningTimesup,File_DiDa='','','',''
File_OnceTimesup_cus,File_AllTimesup_cus,File_WarnningTimesup_cus,File_DiDa_cus='','','',''
blacknormalpointPath,blackhoverpointPath,blackpressedpointPath,blackpoint_spPath='','','',''
settingnormalPath,settinghoverPath,settingpressedPath='','',''
runnormalPath,runhoverPath,runpressedPath='','',''
blacktagrightnormalPath,blacktagrighthoverPath,blacktagrightpressedPath='','',''
blacktagleftnormalPath,blacktaglefthoverPath,blacktagleftpressedPath='','',''

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
        self.slots()                     #等待所有信号
        
    #-------slots--------------
    def go(self):            #环节向前
        global page
        self.sound_AllTimesup.stop()  
        self.sound_OnceTimesup.stop()
        self.sound_DiDa.stop()
        page+=1
        self.fullscreenUI()
        
    def back(self):          #环节退后
        global page
        self.sound_AllTimesup.stop()
        self.sound_OnceTimesup.stop()
        self.sound_DiDa.stop()
        page-=1
        self.fullscreenUI()

        
        
    def UI(self):
        #------widgets-init--------------------
        self.ScreenSize=QDesktopWidget().screenGeometry()
        self.labelcenter=QLabel('',self)               #中央提示文本的label
        self.widgetscenter(self.labelcenter)
        self.labelcenter.show()
        #--------------
        
        self.label_bg=QLabel('',self)
        self.label_bg.setGeometry(0,0,self.ScreenSize.width(),self.ScreenSize.height()) 
        bg_pic=QPixmap(r'picture\bg1.png').scaled(self.ScreenSize.width(),self.ScreenSize.height())
        self.label_bg.setPixmap(bg_pic)
        self.label_bg.lower()
        #--------------------
        window1.showFullScreen()     #以上为全屏UI 以下为控件UI
        #------------------
        palette=QPalette()
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap(r'picture\blackblock.png').scaled(self.view_leftup.width(),self.view_leftup.height())))
        self.view_leftup.setPalette(palette)
        self.view_leftup.setAutoFillBackground(True)
        
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap(r'picture\blackblock.png').scaled(self.view_rightup.width(),self.view_rightup.height())))
        self.view_rightup.setPalette(palette)
        self.view_rightup.setAutoFillBackground(True)
        
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap(r'picture\logo.png').scaled(self.lab_logo.width(),self.lab_logo.height())))
        self.lab_logo.setPalette(palette)
        self.lab_logo.setAutoFillBackground(True)
        
        global blacknormalpointPath,blackhoverpointPath,blackpressedpointPath,blackpoint_spPath
        global settingnormalPath,settinghoverPath,settingpressedPath
        global runnormalPath,runhoverPath,runpressedPath
        global blacktagrightnormalPath,blacktagrighthoverPath,blacktagrightpressedPath
        global blacktagleftnormalPath,blacktaglefthoverPath,blacktagleftpressedPath
        
        blacknormalpointPath=r":/image/btn/blacknormalpoint.png"
        blackhoverpointPath=r":/image/btn/blackhoverpoint.png"
        blackpressedpointPath=r":/image/btn/blackclickpoint.png"
        blackpoint_spPath=r":/image/btn/blackpoint_sp.png"
        
        settingnormalPath=r":/image/btn/settingnormal.png"
        settinghoverPath=r":/image/btn/settinghover.png"
        settingpressedPath=r":/image/btn/settingpressed.png"
        
        runnormalPath=r":/image/btn/runnormal.png"
        runhoverPath=r":/image/btn/runhover.png"
        runpressedPath=r":/image/btn/runpressed.png"
        
        stopnormalPath=r":/image/btn/stopnormal.png"
        stophoverPath=r":/image/btn/stophover.png"
        stoppressedPath=r":/image/btn/stoppressed.png"
        
        blacktagrightnormalPath=r":/image/btn/blacktagrightnormal.png"
        blacktagrighthoverPath=r":/image/btn/blacktagrighthover.png"
        blacktagrightpressedPath=r":/image/btn/blacktagrightpressed.png"
        
        blacktagleftnormalPath=r":/image/btn/blacktagleftnormal.png"
        blacktaglefthoverPath=r":/image/btn/blacktaglefthover.png"
        blacktagleftpressedPath=r":/image/btn/blacktagleftpressed.png"
        
        self.btn_left.setStyleSheet("QPushButton{border-image:url("+blacknormalpointPath+");}"
                              "QPushButton:hover{border-image:url("+blackhoverpointPath+");}"
                              "QPushButton:pressed{border-image:url("+blackpressedpointPath+");}")
        
        self.btn_right.setStyleSheet("QPushButton{border-image:url("+blacknormalpointPath+");}"
                              "QPushButton:hover{border-image:url("+blackhoverpointPath+");}"
                              "QPushButton:pressed{border-image:url("+blackpressedpointPath+");}")
                              
        self.btn_stop.setStyleSheet("QPushButton{border-image:url("+stopnormalPath+");}"
                              "QPushButton:hover{border-image:url("+stophoverPath+");}"
                              "QPushButton:pressed{border-image:url("+stoppressedPath+");}")
                              
        self.btn_run.setStyleSheet("QPushButton{border-image:url("+runnormalPath+");}"
                              "QPushButton:hover{border-image:url("+runhoverPath+");}"
                              "QPushButton:pressed{border-image:url("+runpressedPath+");}")
        self.btn_run.setVisible(False)
        
        self.btn_setting.setStyleSheet("QPushButton{border-image:url("+settingnormalPath+");}"
                              "QPushButton:hover{border-image:url("+settinghoverPath+");}"
                              "QPushButton:pressed{border-image:url("+settingpressedPath+");}")
                              
        self.btn_go.setStyleSheet("QPushButton{border-image:url("+blacktagrightnormalPath+");}"
                              "QPushButton:hover{border-image:url("+blacktagrighthoverPath+");}"
                              "QPushButton:pressed{border-image:url("+blacktagrightpressedPath+");}")
                              
        self.btn_back.setStyleSheet("QPushButton{border-image:url("+blacktagleftnormalPath+");}"
                              "QPushButton:hover{border-image:url("+blacktaglefthoverPath+");}"
                              "QPushButton:pressed{border-image:url("+blacktagleftpressedPath+");}")
                
        
        
       #------widgets-init--------------------
    def inputfile(self):  #载入音频文件
        self.sound_AllTimesup=QSound(File_AllTimesup)
        self.sound_OnceTimesup=QSound(File_OnceTimesup)
        self.sound_DiDa=QSound(File_DiDa)          
                            
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
            else :
                self.sound_AllTimesup.play()
            
        if self.bool_btn_left:                             #判断正方是否在讲话
            if self.ZOnceTime.toString('mm:ss')!='00:00' :  #对正方单次时间的操作
                if QTimeStrToInt(self.ZOnceTime.toString('mm:ss'))<=3:
                    self.sound_DiDa.play()
                self.ZOnceTime=self.ZOnceTime.addSecs(-1)
            else:
                if self.ZAllTime.toString('mm:ss')!='00:00':         
                    self.sound_OnceTimesup.play()
            self.lcd_center.setText(str(QTimeStrToInt(self.ZOnceTime.toString('mm:ss'))))      #显示
        self.lcd_left.setText(self.ZAllTime.toString('mm:ss'))     #显示所有
        
                
        if self.bool_isstart and (self.bool_btn_right or self.bool_right):  #总的开关：是否流逝
            if self.FAllTime.toString('mm:ss')!='00:00' :
                self.FAllTime=self.FAllTime.addSecs(-1)
            else:
                self.sound_AllTimesup.play()
        if self.bool_btn_right:
                
            if self.FOnceTime.toString('mm:ss')!='00:00':
                if QTimeStrToInt(self.FOnceTime.toString('mm:ss'))<=3:
                    self.sound_DiDa.play()
                self.FOnceTime=self.FOnceTime.addSecs(-1)
            else:
                if self.FAllTime.toString('mm:ss')!='00:00':
                    self.sound_OnceTimesup.play()
            self.lcd_center.setText(str(QTimeStrToInt(self.FOnceTime.toString('mm:ss'))))
        self.lcd_right.setText(self.FAllTime.toString('mm:ss'))
        
    def stop(self):
        self.btn_stop.setVisible(False)
        self.btn_run.setVisible(True)
        self.timer.timeout.disconnect(self.update)
    
    def run(self):
        self.btn_run.setVisible(False)
        self.btn_stop.setVisible(True)
        self.timer.timeout.connect(self.update)
        
    def btnleftclick(self):       #正方按钮的效果
        
        if self.bool_btn_left:
            pass
                    
        else:
            if self.bool_isstart==False:
                self.bool_isstart=True
            self.sound_AllTimesup.stop()
            self.sound_OnceTimesup.stop()
            self.sound_DiDa.stop()
            self.ZOnceTime=QTime(0,0,0)
            if self.Var_ZOnceTime <= QTimeStrToInt(self.ZAllTime.toString('mm:ss')):
                self.ZOnceTime=self.ZOnceTime.addSecs(self.Var_ZOnceTime)
            else:
                self.ZOnceTime=self.ZOnceTime.addSecs(QTimeStrToInt(self.ZAllTime.toString('mm:ss')))
            self.btn_left.setStyleSheet("QPushButton{border-image:url("+blackpoint_spPath+");}"
                              "QPushButton:hover{border-image:url("+blackpoint_spPath+");}"
                              "QPushButton:pressed{border-image:url("+blackpoint_spPath+");}")
                              
            self.btn_right.setStyleSheet("QPushButton{border-image:url("+blacknormalpointPath+");}"
                              "QPushButton:hover{border-image:url("+blackhoverpointPath+");}"
                              "QPushButton:pressed{border-image:url("+blackpressedpointPath+");}")
            self.bool_btn_left=True
            self.bool_btn_right=False
            
            
            
            
    def btnrightclick(self):
         if self.bool_btn_right:
            pass
                    
         else:
            if self.bool_isstart==False:
                self.bool_isstart=True
            self.sound_AllTimesup.stop()
            self.sound_OnceTimesup.stop()
            self.sound_DiDa.stop()
            self.FOnceTime=QTime(0,0,0)
            if self.Var_FOnceTime <= QTimeStrToInt(self.FAllTime.toString('mm:ss')):
                self.FOnceTime=self.FOnceTime.addSecs(self.Var_FOnceTime)
            else:
                self.FOnceTime=self.FOnceTime.addSecs(QTimeStrToInt(self.FAllTime.toString('mm:ss')))
            self.btn_right.setStyleSheet("QPushButton{border-image:url("+blackpoint_spPath+");}"
                              "QPushButton:hover{border-image:url("+blackpoint_spPath+");}"
                              "QPushButton:pressed{border-image:url("+blackpoint_spPath+");}")
            
            self.btn_left.setStyleSheet("QPushButton{border-image:url("+blacknormalpointPath+");}"
                              "QPushButton:hover{border-image:url("+blackhoverpointPath+");}"
                              "QPushButton:pressed{border-image:url("+blackpressedpointPath+");}")
            self.bool_btn_right=True
            self.bool_btn_left=False
            
            
            
        
         
                
    #-------slots--------------     #槽函数结束  
    
    def slots(self):      
        self.btn_back.clicked.connect(self.back)
        self.btn_go.clicked.connect(self.go)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_run.clicked.connect(self.run)
    
        
    def keyPressEvent(self,e):#16777216   Esc键
        if e.key() == 16777216:
            '''
            try:
                self.labelcenter.remove()
                del self.labelcenter
            except:
                pass
                
            try:
                
                self.ZOnceTime=QTime(0,0,0)
                self.FOnceTime=QTime(0,0,0)
                self.ZAllTime=QTime(0,0,0)
                self.FAllTime=QTime(0,0,0)
            except:
                pass            
            '''
            #app.quit()
        if e.key() == 81 and self.btn_left.isVisible():
            self.btn_left.clicked.emit()
            
        if e.key() == 69 and self.btn_right.isVisible():
            self.btn_right.clicked.emit()
    
    def widgetscenter(self,widgets):
        screen = QDesktopWidget().screenGeometry()
        size = widgets.geometry()
        widgets.move((screen.width() - size.width()) /2,(screen.height() - size.height())/2)
        
            
    
    def fullscreenUI(self):
        #-----button----
        
        if competition_rules[page][2] =='N':
            self.btn_left.setVisible(False)
            self.btn_left_replace.setVisible(True)
        else:
            self.btn_left.setVisible(True)
            self.btn_left_replace.setVisible(False)
        if competition_rules[page][3] =='N':
            self.btn_right.setVisible(False)
            self.btn_right_replace.setVisible(True)
        else: 
            self.btn_right.setVisible(True)
            self.btn_right_replace.setVisible(False)
        if page == 0:
            self.btn_back.setVisible(False)
            self.btn_back_replace.setVisible(True)
        else:
            self.btn_back.setVisible(True)
            self.btn_back_replace.setVisible(False)
        if page == (len(competition_rules)-1):
            self.btn_go.setVisible(False)
            self.btn_go_replace.setVisible(True)
        else:
            self.btn_go.setVisible(True)
            self.btn_go_replace.setVisible(False)
        if competition_rules[page][10]:
            self.btn_left.clicked.connect(self.lefttip)
        if competition_rules[page][11]:
            self.btn_right.clicked.connect(self.righttip)
            
        self.btn_left.setStyleSheet("QPushButton{border-image:url("+blacknormalpointPath+");}"
                              "QPushButton:hover{border-image:url("+blackhoverpointPath+");}"
                              "QPushButton:pressed{border-image:url("+blackpressedpointPath+");}") 
        self.btn_right.setStyleSheet("QPushButton{border-image:url("+blacknormalpointPath+");}"
                              "QPushButton:hover{border-image:url("+blackhoverpointPath+");}"
                              "QPushButton:pressed{border-image:url("+blackpressedpointPath+");}") 
            
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
            self.ZAllTime,self.FAllTime,self.ZOnceTime,self.FOnceTime=QTime(0,0,0),QTime(0,0,0),QTime(0,0,0),QTime(0,0,0)
            self.lcd_left.setText (self.ZAllTime.toString('mm:ss'))
            self.lcd_right.setText(self.FAllTime.toString('mm:ss'))
            self.lcd_center.setText('00')  
            try:
                self.timer.timeout.disconnect(self.update)
            except:
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
            self.lcd_left.setText(self.ZAllTime.toString('mm:ss'))
            self.lcd_right.setText(self.FAllTime.toString('mm:ss'))
            self.lcd_center.setText('00')            
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
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.signal()    
    def signal (self):
        self.pg1_btn_enter.clicked.connect(self.enter)
        self.pg2_tbtn_filechoose.clicked.connect(self.filechoose)
        self.pg3_btn_01.clicked.connect(self.waitingmusicfile)
        self.pg3_btn_02.clicked.connect(self.medalmusicfile)
        self.pg3_btn_11.clicked.connect(self.timesupvociefile)
        self.pg3_btn_21.clicked.connect(self.warnningvociefile)
        self.pg3_btn_31.clicked.connect(self.didavociefile)
        self.pg3_btn_41.clicked.connect(self.oncespeaktimesupvociefile)
        self.pg4_btn_02.clicked.connect(self.backgroundfile)
        self.pg4_btn_01.clicked.connect(self.showDialog1)
        self.pg4_btn_11.clicked.connect(self.showDialog2)
        self.pg4_btn_12.clicked.connect(self.medalfile)
        self.pg4_btn_21.clicked.connect(self.camp1show)
        self.pg4_btn_22.clicked.connect(self.camp2show)
        self.pg4_btn_31.clicked.connect(self.startpicfile)
        #####
        self.pg3_rbtn_11.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_12.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_13.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_21.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_22.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_23.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_31.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_32.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_33.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_41.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_42.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_43.clicked.connect(self.pg3updatebutton)
        
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
        if competition_rules!=[]:
            
            fullscreenrun()
        else:
            pass
        
    def filechoose(self): 
        global competition_rules
        fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取赛制文件",  nowdir,  "Text Files (*.xlsx)")
        if fileName1 :
            f=xlrd.open_workbook(fileName1)
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
        fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取等待音效文件",  nowdir,  "All Files (*);;Text Files (*.txt)")
        
    
    def medalmusicfile(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取获奖音效文件",  nowdir,  "All Files (*);;Text Files (*.txt)")
        
    
    def timesupvociefile(self):
        global File_AllTimesup_cus
        File_AllTimesup_cus, filetype = QFileDialog.getOpenFileName(self,  "选取总时间到音效文件",  nowdir,  "All Files (*);;Text Files (*.txt)")
        
    
    def warnningvociefile(self):
        File_WarnningTimesup_cus, filetype = QFileDialog.getOpenFileName(self,  "选取警告音效文件",  nowdir,  "All Files (*);;Text Files (*.txt)")
        
    
    def didavociefile(self):
        global File_DiDa_cus
        File_DiDa_cus, filetype = QFileDialog.getOpenFileName(self,  "选取滴答音效文件",  nowdir,  "All Files (*);;Text Files (*.txt)")
        
        
    def oncespeaktimesupvociefile(self):
        global File_OnceTimesup_cus
        File_OnceTimesup_cus, filetype = QFileDialog.getOpenFileName(self,  "选取单次发言时间到音效文件",  nowdir,  "Text Files (*.wav)")
        
        
    def showDialog1(self):
      
        col = QColorDialog.getColor()

    def backgroundfile(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取背景图片文件",  nowdir,  "All Files (*);;Text Files (*.txt)")
        
    def showDialog2(self):
      
        col = QColorDialog.getColor()
     
    def medalfile(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取获奖图片文件",  nowdir,  "All Files (*);;Text Files (*.txt)")
    
    def camp1show(self):
        pass
    
    def camp2show(self):
        pass
    
    def startpicfile (self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,  "选取开场图片文件",  nowdir,  "All Files (*);;Text Files (*.txt)")
    
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
            
    def pg3updatebutton(self):
        
        if self.pg3_rbtn_13.isChecked():
            self.pg3_btn_11.setEnabled(True)
        else:
            self.pg3_btn_11.setEnabled(False)
        
        if self.pg3_rbtn_23.isChecked():
            self.pg3_btn_21.setEnabled(True)
        else:
            self.pg3_btn_21.setEnabled(False)
            
        if self.pg3_rbtn_33.isChecked():
            self.pg3_btn_31.setEnabled(True)
        else:
            self.pg3_btn_31.setEnabled(False)
            
        if self.pg3_rbtn_43.isChecked():
            self.pg3_btn_41.setEnabled(True)
        else:
            self.pg3_btn_41.setEnabled(False)
    #-----------THIS-IS-SLOTS---------------------------
            
            
            
            
def competition_rules_translate(x):
     Vardict=globals()
     
     if isinstance(x,str) and re.match(r'^Var_[0-9a-zA-Z\_]+$',x) and x in Vardict:
         return Vardict[x]
     else:
         return x
                  
 #      pg3_rbtn_34     
def fullscreenrun ():
    global Var_Zname ,Var_Fname,Var_Zviewpoint,Var_Fviewpoint,competition_rules,File_OnceTimesup,File_AllTimesup,File_WarnningTimesup,File_DiDa
    Var_Zname = window.pg1_lineEdit_1.displayText()    
    Var_Fname = window.pg1_lineEdit_2.displayText()
    Var_Zviewpoint = window.pg1_lineEdit_4.displayText()
    Var_Fviewpoint = window.pg1_lineEdit_4.displayText()
    #-------window-value-input------------
    if window.pg3_rbtn_11.isChecked():                        #总时间终止声导入
        File_AllTimesup= r'sound\alltimesup.wav'
    elif window.pg3_rbtn_12.isChecked():
        File_AllTimesup= r'sound\null.wav'
    elif window.pg3_rbtn_13.isChecked():
        File_AllTimesup= File_AllTimesup_cus 
    else:
        File_AllTimesup= r'sound\null.wav'    
    
    if window.pg3_rbtn_41.isChecked():                     #单次发言终止声导入
        File_OnceTimesup= r'sound\oncetimesup.wav'
    elif window.pg3_rbtn_42.isChecked():
        File_OnceTimesup= r'sound\null.wav'
    elif window.pg3_rbtn_43.isChecked():
        File_OnceTimesup= File_OnceTimesup_cus 
    else:
        File_OnceTimesup= r'sound\null.wav'  
        
    
    if window.pg3_rbtn_31.isChecked():                     #倒计时滴答声导入
        File_DiDa= r'sound\dida.wav'
    elif window.pg3_rbtn_32.isChecked():
        File_DiDa= r'sound\null.wav'
    elif window.pg3_rbtn_33.isChecked():
        File_DiDa= File_DiDa_cus 
    else:
        File_DiDa= r'sound\null.wav'  
    #-------window-value-input------------
    window1.inputfile()
    window1.UI()
    for i in range(0,len(competition_rules)):
        competition_rules[i]=list (map(competition_rules_translate,competition_rules[i]))
    window1.fullscreenUI()

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window1 = FullScreen()
    window.show()
    sys.exit(app.exec_())
    
