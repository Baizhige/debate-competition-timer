import sys,os
import re
from PyQt5.QtWidgets import QMainWindow,QApplication,QColorDialog,QPushButton,QDialog,QFileDialog,QLabel,QDesktopWidget,QWidget,QMenu,QFontDialog,QMessageBox
from PyQt5.QtGui import QPixmap,QBrush,QPalette,QIcon,QFont,QCursor
from PyQt5.QtCore import Qt,QTime,QTimer,QSettings,QPropertyAnimation,QStateMachine,QRect,pyqtSlot
from PyQt5.uic import loadUiType
from PyQt5.QtMultimedia import QSound
from images import qpicture
import xlrd
import pickle
import time
import threading


nowdir=sys.argv[0].replace(r'\GUIPyQt.py','')  #debug
#nowdir=''
os.chdir(nowdir)
qtCreatorFile = r'UI\mainwindow.ui'     #导入第一个窗口
Ui_MainWindow,QtBaseClass = loadUiType(qtCreatorFile)
qtCreatorFile1 = r'UI\fullscreen.ui'      #导入第二个窗口
Ui_FullScreen,QtBaseClass1 = loadUiType(qtCreatorFile1)
qtCreatorFile2 = r'UI\seconddialog.ui'      #导入第二个窗口
Ui_Secondwindow,QtBaseClass2 = loadUiType(qtCreatorFile2)


#---global-var--------------------------------------
competition_rules=[]             #赛制
page=0                           #环节
Var_Zname ,Var_Fname,Var_Zviewpoint,Var_Fviewpoint = '','','',''       #基础名字
File_OnceTimesup,File_AllTimesup,File_WarnningTimesup,File_DiDa='','','','' #默认声音文件路径
File_OnceTimesup_cus,File_AllTimesup_cus,File_WarnningTimesup_cus,File_DiDa_cus='','','',''#自定义声音文件路径
blacknormalpointPath,blackhoverpointPath,blackpressedpointPath,blackpoint_spPath='','','',''#UI文件路径
settingnormalPath,settinghoverPath,settingpressedPath='','',''#UI文件路径
runnormalPath,runhoverPath,runpressedPath='','',''#UI文件路径
blacktagrightnormalPath,blacktagrighthoverPath,blacktagrightpressedPath='','',''#UI文件路径
blacktagleftnormalPath,blacktaglefthoverPath,blacktagleftpressedPath='','',''#UI文件路径
Var_custom_1,Var_custom_2,Var_custom_3,Var_custom_4,Var_custom_5,Var_custom_6='','','','','',''#自定义变量初始化
btn_back_awayvisible,btn_go_awayvisible,btn_left_awayvisible,btn_right_awayvisible=True,True,True,True
lcd_left_awayvisible,lcd_right_awayvisible,lcd_center_awayvisible=True,True,True
lab_left_awayvisible,lab_right_awayvisible=True,True

property_size_view_leftup=[380,500]
property_size_view_rightup=[380,500]             #定原始尺寸
view_w_k,view_h_k=0.300000,0.375000

sp_leftuppicPath=r'picture\zhengfang.png'         #后期可以被覆盖
sp_rightuppicPath=r'picture\fanfang.png'
sp_logopicPath=r'picture\logo.png'
sp_bgPath=r'picture\bg1.png'                       #外部引用（方便修改）

blacksheetPath=r":/image/btn/blacksheet.png"              #皮肤包（难以修改）
        
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

mainwindowbgPath=r'picture\mainwindowbg.png'

#---\global-var-----------------------------------------

#---global-function-------------
def QTimeStrToInt(str):               #自定义函数：将QTime类的Qstring 返回成秒
    str+='0'
    
    min=int(str[:2])
    sec=int(str[3:5])
   
    result = min*60+sec

    return result

def QFontSizeSet(qlabel,k):
    tempf=qlabel.font()
    tempf.setPointSize(tempf.pointSize()*k)
    qlabel.setFont(tempf)
    
def competition_rules_translate(x):

     Vardict=globals()
     
     if isinstance(x,str) and re.match(r'^Var_[0-9a-zA-Z\_]+$',x) and x in Vardict:
         return Vardict[x]
     else:
         return x
    
def fullscreenrun ():  #core
    global Var_Zname ,Var_Fname,Var_Zviewpoint,Var_Fviewpoint,competition_rules,File_OnceTimesup,File_AllTimesup,File_WarnningTimesup,File_DiDa
    global Var_custom_1,Var_custom_2,Var_custom_3,Var_custom_4,Var_custom_5,Var_custom_6
    global view_w_k,view_h_k
    Var_Zname = window.pg1_lineEdit_1.displayText()    
    Var_Fname = window.pg1_lineEdit_2.displayText()
    Var_Zviewpoint = window.pg1_lineEdit_4.displayText()
    Var_Fviewpoint = window.pg1_lineEdit_4.displayText()
    
    Var_custom_1 = window.pg6_lineEdit_1.displayText()
    Var_custom_2 = window.pg6_lineEdit_2.displayText()
    Var_custom_3 = window.pg6_lineEdit_3.displayText()
    Var_custom_4 = window.pg6_lineEdit_4.displayText()
    Var_custom_5 = window.pg6_lineEdit_5.displayText()
    Var_custom_6 = window.pg6_lineEdit_6.displayText()
    view_w_k     = float(window.input_view_w_k.displayText())
    view_h_k     = float(window.input_view_h_k.displayText())
    
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

class SecondWindow(QDialog,Ui_Secondwindow):
    def __init__(self):
        QDialog.__init__(self)
        Ui_Secondwindow.__init__(self)
        self.setupUi(self)
        self.slots()
    def slots(self):
        
        self.secdia_pg1_btn_setf.clicked.connect(self.setfont)
        self.secdia_pg1_btn_setc.clicked.connect(self.setcolor)
        
        
        #
        self.secdia_pg2_check_1.clicked.connect(self.setvisible)
        self.secdia_pg2_check_2.clicked.connect(self.setvisible)
        self.secdia_pg2_check_3.clicked.connect(self.setvisible)
        self.secdia_pg2_check_4.clicked.connect(self.setvisible)
        self.secdia_pg2_check_5.clicked.connect(self.setvisible)
        self.secdia_pg2_check_6.clicked.connect(self.setvisible)
        self.secdia_pg2_check_7.clicked.connect(self.setvisible)
        self.secdia_pg2_check_8.clicked.connect(self.setvisible)
        self.secdia_pg2_check_9.clicked.connect(self.setvisible)
        self.secdia_pg2_check_10.clicked.connect(self.setvisible)
        self.secdia_pg2_check_11.clicked.connect(self.setvisible)
        self.secdia_pg2_check_12.clicked.connect(self.setvisible)
        self.secdia_pg2_check_13.clicked.connect(self.setvisible)
        self.secdia_pg2_check_14.clicked.connect(self.setvisible)
        self.secdia_pg2_check_15.clicked.connect(self.setvisible)
        self.secdia_pg2_check_16.clicked.connect(self.setvisible)
        self.secdia_pg2_check_17.clicked.connect(self.setvisible)
        self.secdia_pg2_check_18.clicked.connect(self.setvisible)
        self.secdia_pg2_check_19.clicked.connect(self.setvisible)
        
        
        
    
    def setfont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            if self.lab_leftup1.isChecked():
                window1.lab_leftup1.setFont(font)
            
            if self.lab_leftup2.isChecked():
                window1.lab_leftup2.setFont(font)
                
            if self.lab_leftup3.isChecked():
                window1.lab_leftup3.setFont(font)
                
            if self.lab_rightup1.isChecked():
                window1.lab_rightup1.setFont(font)   
            
            if self.lab_rightup2.isChecked():
                window1.lab_rightup2.setFont(font)   
            
            if self.lab_rightup3.isChecked():
                window1.lab_rightup3.setFont(font) 
            #-----------------
            if self.lab_left.isChecked():
                window1.lab_left.setFont(font)
            
            if self.lab_right.isChecked():
                window1.lab_right.setFont(font)
                
            if self.lab_centerup.isChecked():
                window1.lab_centerup.setFont(font)
                
            if self.lab_center.isChecked():
                window1.lab_center.setFont(font)   
            
            if self.lcd_left.isChecked():
                window1.lcd_left.setFont(font)   
            
            if self.lcd_right.isChecked():
                window1.lcd_right.setFont(font)
            
            if self.lcd_center.isChecked():
                window1.lcd_center.setFont(font)              
            
    
    def setcolor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            if self.lab_leftup1.isChecked():
                window1.lab_leftup1.setStyleSheet('QLabel {color:%s}' % col.name())
            
            if self.lab_leftup2.isChecked():
                window1.lab_leftup2.setStyleSheet('QLabel {color:%s}' % col.name())
                
            if self.lab_leftup3.isChecked():
                window1.lab_leftup3.setStyleSheet('QLabel {color:%s}' % col.name())
                
            if self.lab_rightup1.isChecked():
                window1.lab_rightup1.setStyleSheet('QLabel {color:%s}' % col.name())  
            
            if self.lab_rightup2.isChecked():
                window1.lab_rightup2.setStyleSheet('QLabel {color:%s}' % col.name())
            
            if self.lab_rightup3.isChecked():
                window1.lab_rightup3.setStyleSheet('QLabel {color:%s}' % col.name())
            #-----------------
            if self.lab_left.isChecked():
                window1.lab_left.setStyleSheet('QLabel {color:%s}' % col.name())
            
            if self.lab_right.isChecked():
                window1.lab_right.setStyleSheet('QLabel {color:%s}' % col.name())
                
            if self.lab_centerup.isChecked():
                window1.lab_centerup.setStyleSheet('QLabel {color:%s}' % col.name())
                
            if self.lab_center.isChecked():
                window1.lab_center.setStyleSheet('QLabel {color:%s}' % col.name())
            
            if self.lcd_left.isChecked():
                window1.lcd_left.setStyleSheet('QLabel {color:%s}' % col.name()) 
            
            if self.lcd_right.isChecked():
                window1.lcd_right.setStyleSheet('QLabel {color:%s}' % col.name())
            
            if self.lcd_center.isChecked():
                window1.lcd_center.setStyleSheet('QLabel {color:%s}' % col.name())     
        
    def setvisible(self,e):
        global btn_back_awayvisible,btn_go_awayvisible,btn_left_awayvisible,btn_right_awayvisible,lcd_left_awayvisible,lcd_right_awayvisible,lcd_center_awayvisible
        global lab_left_awayvisible,lab_right_awayvisible
        if  self.secdia_pg2_check_1.isChecked():
            window1.lab_leftup1.setVisible(False)
            window1.lab_leftup1_replace.setVisible(True)
        else:
            window1.lab_leftup1.setVisible(True)
            window1.lab_leftup1_replace.setVisible(False)
        
        if  self.secdia_pg2_check_2.isChecked():
            window1.lab_leftup2.setVisible(False)
            #window1.lab_leftup2_replace.setVisible(True)

        else:
            window1.lab_leftup2.setVisible(True)
            #window1.lab_leftup2_replace.setVisible(False)
        if  self.secdia_pg2_check_3.isChecked():
            #window1.lab_leftup3_replace.setVisible(True)
            window1.lab_leftup3.setVisible(False)
        else:
            #window1.lab_leftup3_replace.setVisible(False)
            window1.lab_leftup3.setVisible(True)
        
        if  self.secdia_pg2_check_4.isChecked():
            window1.lab_rightup1.setVisible(False)
            window1.lab_rightup1_replace.setVisible(True)
        else:
            window1.lab_rightup1.setVisible(True)
            window1.lab_rightup1_replace.setVisible(False)

        if  self.secdia_pg2_check_5.isChecked():
            window1.lab_rightup2.setVisible(False)
            #window1.lab_rightup2_replace.setVisible(True)
        else:
            window1.lab_rightup2.setVisible(True)
            #window1.lab_rightup2_replace.setVisible(False)
        
        if  self.secdia_pg2_check_6.isChecked():
            #window1.lab_rightup3_replace.setVisible(True)
            window1.lab_rightup3.setVisible(False)
        else:
            #window1.lab_rightup3_replace.setVisible(False)
            window1.lab_rightup3.setVisible(True)

        if  self.secdia_pg2_check_7.isChecked():
            window1.lab_centerup.setVisible(False)
            window1.lab_centerup_replace.setVisible(True)
        else:
            window1.lab_centerup.setVisible(True)
            window1.lab_centerup_replace.setVisible(False)
        
        if  self.secdia_pg2_check_8.isChecked():
            lab_left_awayvisible=False
            window1.lab_left_replace.setVisible(True)
            window1.lab_left.setVisible(False)
        else:
            lab_left_awayvisible=True
            window1.lab_left_replace.setVisible(False)
            window1.lab_left.setVisible(True)
        
        if  self.secdia_pg2_check_9.isChecked():
            lab_right_awayvisible=False
            window1.lab_right.setVisible(False)
            window1.lab_right_replace.setVisible(True)
        else:
            lab_right_awayvisible=True
            window1.lab_right_replace.setVisible(False)
            window1.lab_right.setVisible(True)
        
        if  self.secdia_pg2_check_10.isChecked():
            window1.lab_center.setVisible(False)
            window1.lab_center_replace.setVisible(True)
        else:
            window1.lab_center_replace.setVisible(False)
            window1.lab_center.setVisible(True)

        if  self.secdia_pg2_check_11.isChecked():
            btn_back_awayvisible=False
            window1.btn_back.setVisible(False)
            window1.btn_back_replace.setVisible(True)
        else:
            btn_back_awayvisible=True
            window1.btn_back_replace.setVisible(False)
            window1.btn_back.setVisible(True)
        
        if  self.secdia_pg2_check_12.isChecked():
            btn_go_awayvisible=False
            window1.btn_go.setVisible(False)
            window1.btn_go_replace.setVisible(True)
        else:
            btn_go_awayvisible=True
            window1.btn_go_replace.setVisible(False)
            window1.btn_go.setVisible(True)

        if  self.secdia_pg2_check_13.isChecked():
            btn_left_awayvisible=False
            window1.btn_left.setVisible(False)
            window1.btn_left_replace.setVisible(True)
        else:
            btn_left_awayvisible=True
            window1.btn_left.setVisible(True)
            window1.btn_left_replace.setVisible(False)
        
        if  self.secdia_pg2_check_14.isChecked():
            btn_right_awayvisible=False
            window1.btn_right.setVisible(False)
            window1.btn_right_replace.setVisible(True)
        else:
            btn_right_awayvisible=True
            window1.btn_right.setVisible(True)
            window1.btn_right_replace.setVisible(False)
        if  self.secdia_pg2_check_15.isChecked():            #cuz btn_stop is sp
            window1.btn_stop.setVisible(False)
            window1.btn_stop_replace.setVisible(True)
        else:
            if window1.btn_run.isVisible()==False:
                window1.btn_stop.setVisible(True)
                window1.btn_stop_replace.setVisible(False)
        
        if  self.secdia_pg2_check_16.isChecked():
            window1.btn_setting.setVisible(False)
            window1.btn_setting_replace.setVisible(True)
        else:
            window1.btn_setting.setVisible(True)
            window1.btn_setting_replace.setVisible(False)            

        if  self.secdia_pg2_check_17.isChecked():
            lcd_left_awayvisible=False
            window1.lcd_left.setVisible(False)
            window1.lcd_left_replace.setVisible(True)
        else:
            lcd_left_awayvisible=True
            window1.lcd_left.setVisible(True)
            window1.lcd_left_replace.setVisible(False)
            
        if  self.secdia_pg2_check_18.isChecked():
            lcd_right_awayvisible=False
            window1.lcd_center.setVisible(False)
            window1.lcd_center_replace.setVisible(True)
        else:
            lcd_right_awayvisible=True
            window1.lcd_center_replace.setVisible(False)
            window1.lcd_center.setVisible(True)
       
        if  self.secdia_pg2_check_19.isChecked():
            lcd_center_awayvisible=False
            window1.lcd_right_replace.setVisible(True)
            window1.lcd_right.setVisible(False)
        else:
            lcd_center_awayvisible=True
            window1.lcd_right_replace.setVisible(False)
            window1.lcd_right.setVisible(True)                  
            
#---\global-function-------------
class FullScreen(QDialog,Ui_FullScreen):  
    def __init__(self):
        QDialog.__init__(self)
        Ui_FullScreen.__init__(self)
        self.setupUi(self)
        self.slots()                     #为按钮设置信号
        self.createrightclickmenu()
        self.lab_leftup1_replace.setVisible(False)
        self.lab_rightup1_replace.setVisible(False)
        self.lab_left_replace.setVisible(False)
        self.lab_right_replace.setVisible(False)
        self.lab_centerup_replace.setVisible(False)
        self.lab_center_replace.setVisible(False)
        self.lcd_left_replace.setVisible(False)
        self.lcd_right_replace.setVisible(False)
        self.lcd_center_replace.setVisible(False)
        self.btn_stop_replace.setVisible(False)
        self.btn_setting_replace.setVisible(False)
        self.dialog=''
        self.bool_tips=0   #三种值，0，1，2分别对应双方未显示，正方显示，反方显示
        self.bool_tips_used=False
        
        self.ScreenSize=QDesktopWidget().screenGeometry()   #获取全屏数据
        #----widgets----------------------------------
        self.labelcenter=QLabel('',self)         #中央提示文本的label
        font=QFont()
        font.setPointSize(24)
        self.labelcenter.setFont(font)
        self.labelcenter.setStyleSheet("QLabel{border-image:url("+blacksheetPath+");}")
        self.labelcenter.resize(800,400)
        self.labelcenter.setAlignment(Qt.AlignCenter)
        self.widgetscenter(self.labelcenter)
        self.labelcenter.show()
        self.labelcenter.setVisible(False)
        #----widgets-------------------------------
        
        #-----Core--------------------------------
        self.timer=QTimer()
        self.timer.start(100)
        #-----Core----------------------------------
        pass
    
    def widgetscenter(self,widgets):
        screen = QDesktopWidget().screenGeometry()
        size = widgets.geometry()
        widgets.move((screen.width() - size.width()) /2,(screen.height() - size.height())/2)

    def slots(self):      
        self.btn_back.clicked.connect(self.back)
        self.btn_go.clicked.connect(self.go)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_run.clicked.connect(self.run) 
        self.btn_setting.clicked.connect(self.setting)         

    def UI(self):
        
        #------widgets-init--------------------
        #--------------
        global btn_back_awayvisible,btn_go_awayvisible,btn_left_awayvisible,btn_right_awayvisible,lcd_left_awayvisible,lcd_right_awayvisible,lcd_center_awayvisible
        global lab_left_awayvisible,lab_right_awayvisible
        global property_size_view_leftup,property_size_view_rightup
        global view_w_k,view_h_k
        initdata=QSettings(r"settings.ini",QSettings.IniFormat)
        fonts=initdata.value('fonts')
        stylesheets=initdata.value('stylesheets')
        isVisibles=initdata.value('isVisibles')
        a_isVisibles=initdata.value('a_isVisibles')
        
        
        self.label_bg=QLabel('',self)
        self.label_bg.setGeometry(0,0,self.ScreenSize.width(),self.ScreenSize.height()) 
        bg_pic=QPixmap(sp_bgPath).scaled(self.ScreenSize.width(),self.ScreenSize.height())
        self.label_bg.setPixmap(bg_pic)
        self.label_bg.lower()
        #--------------------
        window1.showFullScreen()     #以上为全屏UI 以下为控件UI
        #------------------
        
        
        self.view_leftup.setMinimumSize(self.ScreenSize.width()*view_w_k,self.ScreenSize.height()*view_h_k)
        self.view_rightup.setMinimumSize(self.ScreenSize.width()*view_w_k,self.ScreenSize.height()*view_h_k)
        self.view_leftup.setMaximumSize(self.ScreenSize.width()*view_w_k,self.ScreenSize.height()*view_h_k)
        self.view_rightup.setMaximumSize(self.ScreenSize.width()*view_w_k,self.ScreenSize.height()*view_h_k)
        self.view_leftup.setGeometry(QRect(20,20,self.ScreenSize.width()*view_w_k,self.ScreenSize.height()*view_h_k))
        self.view_rightup.setGeometry(QRect(self.ScreenSize.width()*(1-view_w_k)-20,20,self.ScreenSize.width()*view_w_k,self.ScreenSize.height()*view_h_k))
  
        
        
        property_size_view_leftup[0]=self.view_leftup.width()
        property_size_view_leftup[1]=self.view_leftup.height()
        property_size_view_rightup[0]=self.view_rightup.width()
        property_size_view_rightup[1]=self.view_rightup.height()
        #-----布局
        self.view_center.setGeometry(QRect(10,self.ScreenSize.height()/2-60,self.ScreenSize.width(),self.ScreenSize.height()/2)) 
        self.view_low.setGeometry(QRect(10,self.ScreenSize.height()-70,self.ScreenSize.width()-20,50)) 
        self.view_centerup.setGeometry(QRect((self.ScreenSize.width()-self.view_centerup.width())/2,50,self.view_centerup.width(),self.view_centerup.height()))
        #-----布局

            #--------------------------------
        
        if  isinstance(a_isVisibles[0],str): 
            isVisibles=list(map(lambda x: 'true'==x,isVisibles))
        if  isinstance(a_isVisibles[0],str):    
            a_isVisibles=list(map(lambda x: 'true'==x,a_isVisibles))
        
        print(isVisibles)
        print(a_isVisibles)
        self.lab_leftup1.setFont(fonts[0])
        self.lab_leftup2.setFont(fonts[1])
        self.lab_leftup3.setFont(fonts[2])
        self.lab_left.setFont(fonts[3])
        self.lab_rightup1.setFont(fonts[4])
        self.lab_rightup2.setFont(fonts[5])
        self.lab_rightup3.setFont(fonts[6])
        self.lab_right.setFont(fonts[7])
        self.lcd_left.setFont(fonts[8])
        self.lcd_center.setFont(fonts[9])
        self.lcd_right.setFont(fonts[10])
        self.lab_centerup.setFont(fonts[11])
        self.lab_center.setFont(fonts[12])
        
        self.lab_leftup1.setStyleSheet(stylesheets[0])
        self.lab_leftup2.setStyleSheet(stylesheets[1])
        self.lab_leftup3.setStyleSheet(stylesheets[2])
        self.lab_left.setStyleSheet(stylesheets[3])
        self.lab_rightup1.setStyleSheet(stylesheets[4])
        self.lab_rightup2.setStyleSheet(stylesheets[5])
        self.lab_rightup3.setStyleSheet(stylesheets[6])
        self.lab_right.setStyleSheet(stylesheets[7])
        self.lcd_left.setStyleSheet(stylesheets[8])
        self.lcd_center.setStyleSheet(stylesheets[9])
        self.lcd_right.setStyleSheet(stylesheets[10])
        self.lab_centerup.setStyleSheet(stylesheets[11])
        self.lab_center.setStyleSheet(stylesheets[12])
        
        self.lab_leftup1.setVisible(isVisibles[0])
        self.lab_leftup2.setVisible(isVisibles[1])
        self.lab_leftup3.setVisible(isVisibles[2])
        self.lab_rightup1.setVisible(isVisibles[3])
        self.lab_rightup2.setVisible(isVisibles[4])
        self.lab_rightup3.setVisible(isVisibles[5])
        self.lab_centerup.setVisible(isVisibles[6])
        self.lab_center.setVisible(isVisibles[7])
        
        btn_back_awayvisible   = a_isVisibles[0]
        btn_go_awayvisible     = a_isVisibles[1]
        btn_left_awayvisible   = a_isVisibles[2]
        btn_right_awayvisible  = a_isVisibles[3]
        lcd_left_awayvisible   = a_isVisibles[4]
        lcd_center_awayvisible = a_isVisibles[5]
        lcd_right_awayvisible  = a_isVisibles[6]
        lab_left_awayvisible   = a_isVisibles[7]
        lab_right_awayvisible  = a_isVisibles[8]
     
            #-----------------------------------      
        screen = QDesktopWidget().screenGeometry()
        palette=QPalette()
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap(sp_leftuppicPath).scaled(self.view_leftup.width(),self.view_leftup.height())))
        self.view_leftup.setPalette(palette)
        self.view_leftup.setAutoFillBackground(True)
        self.view_leftup.setGeometry(20,20,property_size_view_leftup[0],property_size_view_leftup[1])

        
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap(sp_rightuppicPath).scaled(self.view_rightup.width(),self.view_rightup.height())))
        self.view_rightup.setPalette(palette)
        self.view_rightup.setAutoFillBackground(True)
        self.view_rightup.setGeometry(self.ScreenSize.width()-property_size_view_rightup[0]-20,20,property_size_view_rightup[0],property_size_view_rightup[1])
        
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap(sp_logopicPath).scaled(self.lab_logo.width(),self.lab_logo.height())))
        self.lab_logo.setPalette(palette)
        self.lab_logo.setAutoFillBackground(True)
        '''
        global blacknormalpointPath,blackhoverpointPath,blackpressedpointPath,blackpoint_spPath
        global settingnormalPath,settinghoverPath,settingpressedPath
        global runnormalPath,runhoverPath,runpressedPath
        global blacktagrightnormalPath,blacktagrighthoverPath,blacktagrightpressedPath
        global blacktagleftnormalPath,blacktaglefthoverPath,blacktagleftpressedPath
        '''
        
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
        pass

    def inputfile(self):  #载入音频文件
        self.sound_AllTimesup=QSound(File_AllTimesup)
        self.sound_OnceTimesup=QSound(File_OnceTimesup)
        self.sound_DiDa=QSound(File_DiDa)     


    def closeEvent(self,event):
        
        reply = QMessageBox.question(self, '提示',
            "你确定要结束辩论赛吗？", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply==QMessageBox.Yes:
            global page
            page=0
            try:
                self.timer.timeout.disconnect(self.update)
            except:
                pass
            try:
                del self.ZOnceTime,self.FOnceTime,self.ZAllTime,self.FAllTime
                self.ZOnceTime=QTime(0,0,0)
                self.FOnceTime=QTime(0,0,0)
                self.ZAllTime=QTime(0,0,0)
                self.FAllTime=QTime(0,0,0)
            except:
                pass    
            
            self.bool_tips=0 
            #print ("此时的布尔值为：",self.bool_tips)
            self.view_leftup.setGeometry(QRect(20,20,property_size_view_leftup[0],property_size_view_leftup[0]) )
            self.view_rightup.setGeometry(QRect(self.ScreenSize.width()-property_size_view_leftup[0]-20,20,property_size_view_leftup[0],property_size_view_leftup[0]))         
            palette=QPalette()
            palette.setBrush(self.backgroundRole(),QBrush(QPixmap(sp_rightuppicPath).scaled(self.view_rightup.width(),self.view_rightup.height())))
            self.view_rightup.setPalette(palette)
            self.view_rightup.setAutoFillBackground(True)
            self.view_rightup.setGeometry(self.ScreenSize.width()-property_size_view_rightup[0]-20,20,property_size_view_rightup[0],property_size_view_rightup[1])
        
            palette.setBrush(self.backgroundRole(),QBrush(QPixmap(sp_logopicPath).scaled(self.lab_logo.width(),self.lab_logo.height())))
            self.lab_logo.setPalette(palette)
            self.lab_logo.setAutoFillBackground(True)
        
            self.btn_stop.setVisible(True)
            self.btn_run.setVisible(False)
            
        
            event.accept()
        else:
            event.ignore()        
#-------slots--------------
    def go(self):            #环节向前
        global page
        if self.bool_tips==0:
            self.sound_AllTimesup.stop()  
            self.sound_OnceTimesup.stop()
            self.sound_DiDa.stop()
            page+=1
            self.fullscreenUI()
        
    def back(self):          #环节退后
        global page
        if self.bool_tips==0:
            self.sound_AllTimesup.stop()
            self.sound_OnceTimesup.stop()
            self.sound_DiDa.stop()
            page-=1
            self.fullscreenUI()
    
    def tool_palette_l(self):
        palette=QPalette()
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap(sp_leftuppicPath).scaled(property_size_view_leftup[0],property_size_view_leftup[1])))
        self.view_leftup.setPalette(palette)
        
    def tool_palette_r(self):
        palette=QPalette()
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap(sp_rightuppicPath).scaled(property_size_view_rightup[0],property_size_view_rightup[1])))
        self.view_rightup.setPalette(palette)
        
    def tool_setfont2_l(self):
        QFontSizeSet(self.lab_leftup1,2)
        QFontSizeSet(self.lab_leftup2,2)
        QFontSizeSet(self.lab_leftup3,2)
        
    def tool_setfont2_r(self):
        QFontSizeSet(self.lab_rightup1,2)
        QFontSizeSet(self.lab_rightup2,2)
        QFontSizeSet(self.lab_rightup3,2)
        
    def tool_checkused(self):
        self.bool_tips_used=False
        
    def tool_connect_r(self):
        self.btn_left.clicked.connect(self.righttip)
    @pyqtSlot()       
    def lefttip(self):      #提醒按键
        if self.bool_tips_used==False:
            self.bool_tips_used=True
            threading.Timer(1,self.tool_checkused).start()
            #self.labelcenter.setVisible(True)
        #-----
            #self.lab_center.setText(str(self.view_leftup.maximumHeight()))
            screen = QDesktopWidget().screenGeometry()
            if self.bool_tips==0:
                pass
            elif self.bool_tips==1:
                QFontSizeSet(self.lab_leftup1,0.5)
                QFontSizeSet(self.lab_leftup2,0.5)
                QFontSizeSet(self.lab_leftup3,0.5)
                #self.view_leftup.resize(property_size_view_leftup[0],property_size_view_leftup[1])
                
                
                #self.view_leftup.setMaximumWidth(property_size_view_leftup[0])
                #self.view_leftup.setMaximumHeight(property_size_view_leftup[1])
                
                
                self.view_leftup.setMaximumSize(property_size_view_leftup[0],property_size_view_leftup[1])
                
                o_rect=QRect((screen.width() - property_size_view_leftup[0]*2) /2,(screen.height() - property_size_view_leftup[1]*2)/2,property_size_view_leftup[0]*2,property_size_view_leftup[1]*2)           
                e_rect=QRect(20,20,property_size_view_leftup[0],property_size_view_leftup[0])
                self.animation = QPropertyAnimation(self.view_leftup,b'geometry' )        
                self.animation.setDuration(400)
                self.animation.setStartValue(o_rect)
                self.animation.setEndValue(e_rect)
                self.animation.start()
            
            
                self.bool_tips=0
                t=threading.Timer(0.4,self.tool_palette_l)
                t.start()
                
                '''
                time.sleep(0.4)
                palette=QPalette()
                palette.setBrush(self.backgroundRole(),QBrush(QPixmap(sp_leftuppicPath).scaled(property_size_view_leftup[0],property_size_view_leftup[1])))
                self.view_leftup.setPalette(palette)
                '''
                return 0
            
            elif self.bool_tips==2:
                #self.view_rightup.resize(property_size_view_rightup[0],property_size_view_rightup[1])
                
                #self.view_rightup.setMaximumWidth(property_size_view_rightup[0])
                #self.view_rightup.setMaximumHeight(property_size_view_rightup[1])
                
                QFontSizeSet(self.lab_rightup1,0.5)
                QFontSizeSet(self.lab_rightup2,0.5)
                QFontSizeSet(self.lab_rightup3,0.5) 
                self.view_rightup.setMaximumSize(property_size_view_leftup[0],property_size_view_leftup[1])

                self.view_rightup.setGeometry(screen.width()-property_size_view_rightup[0]-20,20,property_size_view_rightup[0],property_size_view_rightup[0])
                palette=QPalette()
                palette.setBrush(self.backgroundRole(),QBrush(QPixmap(sp_rightuppicPath).scaled(property_size_view_rightup[0],property_size_view_rightup[1])))
                self.view_rightup.setPalette(palette)
                
            
             
            
            
            #self.view_leftup.resize(property_size_view_leftup[0]*2,property_size_view_leftup[1]*2)
            
            #self.view_leftup.setMaximumWidth(property_size_view_leftup[0]*2)
            #self.view_leftup.setMaximumHeight(property_size_view_leftup[1]*2)
            
           
            self.view_leftup.setMaximumSize(99999,99999)

            o_rect=QRect(0,0,property_size_view_leftup[0],property_size_view_rightup[0])
            e_rect=QRect((screen.width() - property_size_view_leftup[0]*2) /2,(screen.height() - property_size_view_leftup[1]*2)/2,property_size_view_leftup[0]*2,property_size_view_leftup[1]*2)           
            self.animation = QPropertyAnimation(self.view_leftup,b'geometry' )        
            self.animation.setDuration(800)
            self.animation.setStartValue(o_rect)
            self.animation.setEndValue(e_rect)
            self.animation.start()
            t=threading.Timer(0.8,self.tool_setfont2_l)
            t.start()
            
            
            self.bool_tips=1
            '''
            t=threading.Timer(0.8,self.tool_palette_l)
            t.start()
            '''
            #time.sleep(0.8)
            palette=QPalette()
            palette.setBrush(self.backgroundRole(),QBrush(QPixmap(sp_leftuppicPath).scaled(property_size_view_leftup[0]*2,property_size_view_leftup[1]*2)))
            self.view_leftup.setPalette(palette)
            
        #---------
            
            #self.labelcenter.setText(competition_rules[page][10])
    @pyqtSlot()    
    def righttip(self):     #提醒按键
        if self.bool_tips_used==False:
            self.bool_tips_used=True
            threading.Timer(1,self.tool_checkused).start()
            #self.lab_center.setText(str(self.view_rightup.maximumHeight()))
            screen = QDesktopWidget().screenGeometry()
            if self.bool_tips==0:
                pass
            elif self.bool_tips==2:
                QFontSizeSet(self.lab_rightup1,0.5)
                QFontSizeSet(self.lab_rightup2,0.5)
                QFontSizeSet(self.lab_rightup3,0.5) 
                
                #self.view_rightup.resize(property_size_view_rightup[0],property_size_view_rightup[1])
                
                #self.view_rightup.setMinimumSize(property_size_view_rightup[0],property_size_view_rightup[1])
                
                #self.view_rightup.setMaximumWidth(property_size_view_rightup[0])
                #self.view_rightup.setMaximumHeight(property_size_view_rightup[1])
                
                self.view_rightup.setMaximumSize(property_size_view_rightup[0],property_size_view_rightup[1])
                o_rect=QRect((screen.width() - property_size_view_rightup[0]*2) /2,(screen.height() - property_size_view_rightup[1]*2)/2,property_size_view_rightup[0]*2,property_size_view_rightup[1]*2)
                e_rect=QRect(screen.width()-property_size_view_rightup[0]-20,20,property_size_view_rightup[0],property_size_view_rightup[1])                
                self.animation = QPropertyAnimation(self.view_rightup,b'geometry' )        
                self.animation.setDuration(400)
                self.animation.setStartValue(o_rect)
                self.animation.setEndValue(e_rect)
                self.animation.start()
                self.bool_tips=0
                t=threading.Timer(0.4,self.tool_palette_r)
                t.start()
                '''
                time.sleep(0.4)
                palette=QPalette()
                palette.setBrush(self.backgroundRole(),QBrush(QPixmap(sp_rightuppicPath).scaled(property_size_view_rightup[0],property_size_view_rightup[1])))
                self.view_rightup.setPalette(palette)
                '''
                return 0
            
            elif self.bool_tips==1:
                #self.view_leftup.resize(property_size_view_leftup[0],property_size_view_leftup[1])
                #self.view_leftup.setMinimumSize(property_size_view_leftup[0],property_size_view_leftup[1])
                
                #self.view_leftup.setMaximumWidth(property_size_view_leftup[0])
                #self.view_leftup.setMaximumHeight(property_size_view_leftup[1])
                
                QFontSizeSet(self.lab_leftup1,0.5)
                QFontSizeSet(self.lab_leftup2,0.5)
                QFontSizeSet(self.lab_leftup3,0.5)
                
                self.view_leftup.setGeometry(20,20,property_size_view_leftup[0],property_size_view_leftup[0])
                palette=QPalette()
                palette.setBrush(self.backgroundRole(),QBrush(QPixmap(sp_leftuppicPath).scaled(property_size_view_leftup[0],property_size_view_leftup[1])))
                self.view_leftup.setPalette(palette)

            
            
            #self.view_rightup.resize(property_size_view_rightup[0]*2,property_size_view_rightup[1]*2)
            #self.view_rightup.setMinimumSize(property_size_view_rightup[0]*2,property_size_view_rightup[1]*2)
            
            #self.view_rightup.setMaximumWidth(property_size_view_rightup[0]*2)
            #self.view_rightup.setMaximumHeight(property_size_view_rightup[1]*2)
            
            
            self.view_rightup.setMaximumSize(99999,99999)
            o_rect=QRect(screen.width()-property_size_view_rightup[0]-20,20,property_size_view_rightup[0],property_size_view_rightup[1])                
            e_rect=QRect((screen.width() - property_size_view_rightup[0]*2) /2,(screen.height() - property_size_view_rightup[1]*2)/2,property_size_view_rightup[0]*2,property_size_view_rightup[1]*2)
            self.animation = QPropertyAnimation(self.view_rightup,b'geometry' )        
            self.animation.setDuration(800)
            self.animation.setStartValue(o_rect)
            self.animation.setEndValue(e_rect)
            self.animation.start()
            self.bool_tips=2
            
            
            #time.sleep(0.8)
            palette=QPalette()
            palette.setBrush(self.backgroundRole(),QBrush(QPixmap(sp_rightuppicPath).scaled(property_size_view_rightup[0]*2,property_size_view_rightup[1]*2)))
            self.view_rightup.setPalette(palette)
            t=threading.Timer(0.8,self.tool_setfont2_r)
            t.start()
            #self.labelcenter.setText(competition_rules[page][11])
    
    def setting(self):
        self.showcontextmenu()
    
    def update(self):       #每秒执行一次的槽函数   （核心）
        if self.bool_isstart and (self.bool_btn_left or self.bool_left):  #总的开关：是否流逝
            if self.ZAllTime.toString('mm:ss')!='00:00':  #对正方所有时间的操作
                self.ZAllTime=self.ZAllTime.addMSecs(-100)
            else :
                if self.sound_AllTimesup.isFinished():
                    self.sound_AllTimesup.play()
            
        if self.bool_btn_left:                              #判断正方是否在讲话
            if self.ZOnceTime.toString('mm:ss')!='00:00' :  #对正方单次时间的操作
                if QTimeStrToInt(self.ZOnceTime.toString('mm:ss'))<=3 and self.sound_DiDa.isFinished():
                    self.sound_DiDa.play()
                self.ZOnceTime=self.ZOnceTime.addMSecs(-100)
            else:
                if self.ZAllTime.toString('mm:ss')!='00:00' and self.sound_OnceTimesup.isFinished():         
                    self.sound_OnceTimesup.play()
            self.lcd_center.setText(str(QTimeStrToInt(self.ZOnceTime.toString('mm:ss'))))      #显示
        self.lcd_left.setText(self.ZAllTime.toString('mm:ss'))     #显示所有
        
                
        if self.bool_isstart and (self.bool_btn_right or self.bool_right):  #总的开关：是否流逝
            if self.FAllTime.toString('mm:ss')!='00:00' :
                self.FAllTime=self.FAllTime.addMSecs(-100)
            else:
                if self.sound_AllTimesup.isFinished():
                    self.sound_AllTimesup.play()
        if self.bool_btn_right:
                
            if self.FOnceTime.toString('mm:ss')!='00:00':
                if QTimeStrToInt(self.FOnceTime.toString('mm:ss'))<=3 and self.sound_DiDa.isFinished():
                    self.sound_DiDa.play()
                self.FOnceTime=self.FOnceTime.addMSecs(-100)
            else:
                if self.FAllTime.toString('mm:ss')!='00:00' and self.sound_OnceTimesup.isFinished():
                    self.sound_OnceTimesup.play()
            self.lcd_center.setText(str(QTimeStrToInt(self.FOnceTime.toString('mm:ss'))))
        self.lcd_right.setText(self.FAllTime.toString('mm:ss'))
        
    def voicecontrol(self):
        pass
        
    def stop(self):
        self.btn_stop.setVisible(False)
        self.btn_run.setVisible(True)
        try:
            self.timer.timeout.disconnect(self.update)
        except:
            pass
    def run(self):
        self.btn_run.setVisible(False)
        self.btn_stop.setVisible(True)
        if competition_rules[page][5] !='N':
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
    
    def freepaint(self):
        if page==0:
            if self.dialog=='':
                self.dialog=SecondWindow()
                self.dialog.setFixedSize(506,482)
                #self.dialog.setWindowFlags(Qt.FramelessWindowHint)
                self.dialog.show()
            else:
                self.dialog.show()
            
#-------\slots--------------     #槽函数结束  
    def keyPressEvent(self,e):#16777216   Esc键
        if e.key() == 16777216:
            self.close()
            
        if e.key() == 81 and competition_rules[page][2] !='N':
            self.btn_left.clicked.emit()
            
        if e.key() == 69 and competition_rules[page][3] !='N': 
            self.btn_right.clicked.emit()
        
        if e.key() == 54 and page != (len(competition_rules)-1): #6键
            self.btn_go.clicked.emit()
        if e.key() == 52 and page != 0: #4键
            self.btn_back.clicked.emit()
        
        if e.key() == 96 :
            pass
            #self.labelcenter.setVisible(False)

    def saveandclose(self):
        global page
        page=0
        try:
            self.timer.timeout.disconnect(self.update)
        except:
            pass
        try:
            del self.ZOnceTime,self.FOnceTime,self.ZAllTime,self.FAllTime
            self.ZOnceTime=QTime(0,0,0)
            self.FOnceTime=QTime(0,0,0)
            self.ZAllTime=QTime(0,0,0)
            self.FAllTime=QTime(0,0,0)
        except:
            pass    
        
        self.bool_tips=0 
        self.view_leftup.setGeometry(QRect(20,20,property_size_view_leftup[0],property_size_view_leftup[0]) )
        self.view_rightup.setGeometry(QRect(self.ScreenSize.width()-property_size_view_leftup[0]-20,20,property_size_view_leftup[0],property_size_view_leftup[0]))         
        palette=QPalette()
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap(sp_rightuppicPath).scaled(self.view_rightup.width(),self.view_rightup.height())))
        self.view_rightup.setPalette(palette)
        self.view_rightup.setAutoFillBackground(True)
        self.view_rightup.setGeometry(self.ScreenSize.width()-property_size_view_rightup[0]-20,20,property_size_view_rightup[0],property_size_view_rightup[1])
        
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap(sp_logopicPath).scaled(self.lab_logo.width(),self.lab_logo.height())))
        self.lab_logo.setPalette(palette)
        self.lab_logo.setAutoFillBackground(True)
        
        self.btn_stop.setVisible(True)
        self.btn_run.setVisible(False)
            
        self.close()
            
            
    def createrightclickmenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showcontextmenu)  
        self.contextMenu=QMenu(self)
        self.action1 = self.contextMenu.addAction(QIcon(''),u'自定义美化')
        self.action2 = self.contextMenu.addAction(QIcon(''),u'保存设置')
        self.action3 = self.contextMenu.addAction(QIcon(''),u'退出辩论赛')
        self.action1.triggered.connect(self.freepaint)
        self.action2.triggered.connect(self.saveall)
        self.action3.triggered.connect(self.saveandclose)
        
       
    def showcontextmenu(self):
        self.contextMenu.exec_(QCursor.pos())
        #self.contextMenu.show()
    
    def saveall(self):
        savedata=QSettings(r"settings.ini",QSettings.IniFormat)
        fonts=[window1.lab_leftup1.font(),window1.lab_leftup2.font(),window1.lab_leftup3.font(),window1.lab_left.font(),window1.lab_rightup1.font(),window1.lab_rightup2.font(),window1.lab_rightup3.font(),window1.lab_right.font(),window1.lcd_left.font(),window1.lcd_center.font(),window1.lcd_right.font(),window1.lab_centerup.font(),window1.lab_center.font()]
        stylesheets=[window1.lab_leftup1.styleSheet(),window1.lab_leftup2.styleSheet(),window1.lab_leftup3.styleSheet(),window1.lab_left.styleSheet(),window1.lab_rightup1.styleSheet(),window1.lab_rightup2.styleSheet(),window1.lab_rightup3.styleSheet(),window1.lab_right.styleSheet(),window1.lcd_left.styleSheet(),window1.lcd_center.styleSheet(),window1.lcd_right.styleSheet(),window1.lab_centerup.styleSheet(),window1.lab_center.styleSheet()]
        isVisibles=[window1.lab_leftup1.isVisible(),window1.lab_leftup2.isVisible(),window1.lab_leftup3.isVisible(),window1.lab_rightup1.isVisible(),window1.lab_rightup2.isVisible(),window1.lab_rightup3.isVisible(),window1.lab_centerup.isVisible(),window1.lab_center.isVisible()]
        a_isVisibles=[btn_back_awayvisible,btn_go_awayvisible,btn_left_awayvisible,btn_right_awayvisible,lcd_left_awayvisible,lcd_center_awayvisible,lcd_right_awayvisible,lab_left_awayvisible,lab_right_awayvisible]
        k=[view_w_k,view_h_k]
        savedata.setValue("fonts",fonts)
        savedata.setValue("stylesheets",stylesheets)
        savedata.setValue("isVisibles",isVisibles)
        savedata.setValue("a_isVisibles",a_isVisibles)
        savedata.setValue("k",k)
        '''
        savedata=open(r"save.pkl",'wb')
        L=[1,2,3]
        fonts=[window1.lab_leftup1.font(),window1.lab_leftup2.font(),window1.lab_leftup3.font(),window1.lab_left.font(),window1.lab_rightup1.font(),window1.lab_rightup2.font(),window1.lab_rightup3.font(),window1.lab_right.font(),window1.lcd_left.font(),window1.lcd_center.font(),window1.lcd_right.font()]
        pickle.dump(fonts,savedata)
        savedata.close()
        '''
     
    
    def fullscreenUI(self):  #core
        #--------二次进入绑定清零---
        try:
            self.timer.timeout.disconnect(self.update)  #avoid connect again
        except:
            pass
            
        try:
            print("准备取消连接了") 
            self.btn_left.clicked.disconnect(self.lefttip)
            self.btn_right.clicked.disconnect(self.righttip)
            print("取消连接了")            #avoid connect again
        except:
            pass
         
        
        #-------------------    
        self.lcd_center.setVisible(True)
        #-----button----
        
        if competition_rules[page][2] =='N':
            self.btn_left.setVisible(False)
            self.btn_left_replace.setVisible(True)
        else:
            print (btn_left_awayvisible)
            if btn_left_awayvisible:
                self.btn_left.setVisible(True)
                self.btn_left_replace.setVisible(False)
        if competition_rules[page][3] =='N':
            self.btn_right.setVisible(False)
            self.btn_right_replace.setVisible(True)
        else: 
            if btn_right_awayvisible:
                self.btn_right.setVisible(True)
                self.btn_right_replace.setVisible(False)
        if page == 0:
            self.btn_back.setVisible(False)
            self.btn_back_replace.setVisible(True)
        else:
            if btn_back_awayvisible:
                self.btn_back.setVisible(True)
                self.btn_back_replace.setVisible(False)
        if page == (len(competition_rules)-1):
            self.btn_go.setVisible(False)
            self.btn_go_replace.setVisible(True)
        else:
            if btn_go_awayvisible:
                self.btn_go.setVisible(True)
                self.btn_go_replace.setVisible(False)
        if competition_rules[page][10]:
            self.lcd_center.setVisible(False)
            self.btn_go.setVisible(False)
            self.btn_back.setVisible(False)
            self.btn_left.clicked.connect(self.lefttip)
        if competition_rules[page][11]:
            self.lcd_center.setVisible(False)
            self.btn_go.setVisible(False)
            self.btn_back.setVisible(False)
            self.btn_right.clicked.connect(self.righttip)
            
        self.btn_left.setStyleSheet("QPushButton{border-image:url("+blacknormalpointPath+");}"
                              "QPushButton:hover{border-image:url("+blackhoverpointPath+");}"
                              "QPushButton:pressed{border-image:url("+blackpressedpointPath+");}") 
        self.btn_right.setStyleSheet("QPushButton{border-image:url("+blacknormalpointPath+");}"
                              "QPushButton:hover{border-image:url("+blackhoverpointPath+");}"
                              "QPushButton:pressed{border-image:url("+blackpressedpointPath+");}") 
                              
        self.btn_stop.setVisible(True)
        self.btn_run.setVisible(False)              
            
        #-----\button----
        
        #-----label-----
        
        
        self.labelcenter.setVisible(False)  
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
        #-----\label-----
        
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
            
        #-----\lcdnumber-----
        pass
       
class MyApp(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.signal()    
        initdata=QSettings(r"settings.ini",QSettings.IniFormat)
        k=initdata.value('k')
        self.input_view_w_k.setText(str(k[0]))
        self.input_view_h_k.setText(str(k[1]))
        self.setWindowFlags(Qt.FramelessWindowHint)
        palette=QPalette()
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap(mainwindowbgPath).scaled(self.width(),self.height())))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
    
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_drag=True
            self.m_DragPosition=event.globalPos()-self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag=False
        self.setCursor(QCursor(Qt.ArrowCursor))
    def signal (self):
        self.pg1_btn_enter.clicked.connect(self.enter)
        self.pg2_tbtn_filechoose.clicked.connect(self.filechoose)
        #self.pg3_btn_01.clicked.connect(self.waitingmusicfile)
        #self.pg3_btn_02.clicked.connect(self.medalmusicfile)
        #self.pg3_btn_11.clicked.connect(self.timesupvociefile)
        #self.pg3_btn_21.clicked.connect(self.warnningvociefile)
        #self.pg3_btn_31.clicked.connect(self.didavociefile)
        #self.pg3_btn_41.clicked.connect(self.oncespeaktimesupvociefile)
        #self.pg4_btn_02.clicked.connect(self.backgroundfile)
        #self.pg4_btn_01.clicked.connect(self.showDialog1)
        #self.pg4_btn_11.clicked.connect(self.showDialog2)
        #self.pg4_btn_12.clicked.connect(self.medalfile)
        #self.pg4_btn_21.clicked.connect(self.camp1show)
        #self.pg4_btn_22.clicked.connect(self.camp2show)
        #self.pg4_btn_31.clicked.connect(self.startpicfile)
        #####
        self.pg3_rbtn_11.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_12.clicked.connect(self.pg3updatebutton)
        #self.pg3_rbtn_13.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_21.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_22.clicked.connect(self.pg3updatebutton)
        #self.pg3_rbtn_23.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_31.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_32.clicked.connect(self.pg3updatebutton)
        #self.pg3_rbtn_33.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_41.clicked.connect(self.pg3updatebutton)
        self.pg3_rbtn_42.clicked.connect(self.pg3updatebutton)
        #self.pg3_rbtn_43.clicked.connect(self.pg3updatebutton)
        
        #self.pg4_rbtn_01.clicked.connect(self.pg4updatebutton)
        #self.pg4_rbtn_02.clicked.connect(self.pg4updatebutton)
        #self.pg4_rbtn_03.clicked.connect(self.pg4updatebutton)
        #self.pg4_rbtn_11.clicked.connect(self.pg4updatebutton)
        #self.pg4_rbtn_12.clicked.connect(self.pg4updatebutton)
        #self.pg4_rbtn_13.clicked.connect(self.pg4updatebutton)
        #####
        
        
        
    #-----------SLOTS---------------------------
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
            reply = QMessageBox.warning(self,
                                    "温馨提醒",  
                                    "请使用左上角的按钮导入赛制文件"  )
        
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
            reply = QMessageBox.warning(self,
                                    "温馨提醒",  
                                    "没有读取到xlsx文件,请重新读取"  )
                 
    
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
            
        '''if self.pg4_rbtn_12.isChecked():
            self.pg4_btn_11.setEnabled(True)
        else:
            self.pg4_btn_11.setEnabled(False)
            
        if self.pg4_rbtn_13.isChecked():
            self.pg4_btn_12.setEnabled(True)
        else:
            self.pg4_btn_12.setEnabled(False)
        '''    
    def pg3updatebutton(self):
        '''
        if self.pg3_rbtn_13.isChecked():
            #self.pg3_btn_11.setEnabled(True)
        else:
            #self.pg3_btn_11.setEnabled(False)
        
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
        '''    
    #-----------\SLOTS---------------------------


if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    window1 = FullScreen()
    sys.exit(app.exec_())
    
    
