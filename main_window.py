#coding:utf8
'''
主窗口
'''
import os
import sys
import cv2
import numpy as np

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
from PyQt4 import QtCore

from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)


from auto_tm import Auto_tm
from manual_tm import Manual_tm
from sample import Sample
from element import Element

#所有ui
import new_main_window

#所有的class 
from setting_dlg_class import setting_Dialog
from tmpl_setting_dlg_class import set_paper_Dialog
from add_element_dlg_class import add_element_Dialog

from globals import *
from myutils import _fromUtf8,alert,confirm,get_resource,\
            get_relative_dir
#from myutils import *


QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
Windows = sys.platform.lower().startswith(("win", "microsoft"))


class new_main_window(QMainWindow, new_main_window.Ui_MainWindow):
    """
    #图像操作的主窗口
    """               
    def __init__(self,parent=None):
        super(new_main_window, self).__init__(None)
        self.setupUi(self)
        #设置默认值
        self.set_default_values()
        #添加图片能显示的组件，主要是matplot元素
        self.add_draw_canvas()
        #定义所有事件
        self.add_events()
        
        #初始化界面元素
        self.init_gui()
        
        
    def set_default_values(self):
        #self.resize(800, 400)  #把主窗口设置成这样大      
        self.showMaximized() #最大化
        self.setWindowTitle(_fromUtf8("图像操作窗"))
        self.updating = 'no' #界面初始化为没有实时更新
        self.paper_threshold = 150 #纸张的默认阀值
        
        
        #新建模板窗口
        self.set_paper_Dialog   = set_paper_Dialog(self)
        #添加元素窗口
        self.add_element_Dialog = add_element_Dialog(self)
        #全局设置
        self.setting_Dialog     = setting_Dialog(self)
        

    def add_draw_canvas(self): 
        """添加画图元素"""
        #初始化载入的图像 
        self.main_frame = QWidget()
        
        #这里可以把QWidget的大小设置成功
        #self.setMinimumSize(1200, 900)
        #self.setMaximumSize(1200, 900)        
                
        self.fig = Figure((10.0, 10.0), dpi=dpi) #这里不知道怎么设置好
        self.canvas = FigureCanvas(self.fig)   
            
        self.canvas.setParent(self.main_frame)
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        self.canvas.mpl_connect('key_press_event', self.on_key_press) #matplotlib的键盘事件
        self.canvas.mpl_connect('button_press_event', self.onclick) 
        
        self.canvas.setContextMenuPolicy(Qt.CustomContextMenu)
        self.canvas.customContextMenuRequested.connect(self.showMenu)            
        
        #去掉旧的self.myImageLabel，加上新的canvas
        self.verticalLayout.removeWidget(self.myImageLabel)
        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout.addWidget(self.mpl_toolbar)                     


    def add_events(self):
        """
        "自定义一些事件
        """
        #全局设置
        self.connect(self.settingAction,    SIGNAL("triggered()"),      self.global_set)
        #添加新元素
        self.connect(self.addAction,        SIGNAL("triggered()"),      self.add_element)
        #去掉选中元素
        self.connect(self.removeAction,     SIGNAL("triggered()"),      self.remove_element)
        
        #方向键的使用
        self.connect(self.upAction,         SIGNAL("triggered()"),      self.up_moved)
        self.connect(self.downAction,       SIGNAL("triggered()"),      self.down_moved)
        self.connect(self.leftAction,       SIGNAL("triggered()"),      self.left_moved)
        self.connect(self.rightAction,      SIGNAL("triggered()"),      self.right_moved)
        
        #新建模板
        self.connect(self.create_tm_action, SIGNAL("triggered()"),      self.create_tmpl)        
        #拍照事件
        self.connect(self.captureAction,    SIGNAL("triggered()"),      self.capture_action)
        #切换摄像头
        self.connect(self.switch_cap_action,SIGNAL("triggered()"),      self.switch_camra)  
        #打开摄像头
        self.connect(self.open_camera_action,SIGNAL("triggered()"),     self.open_camera) 
        self.connect(self.close_cam_action, SIGNAL("triggered()"),      self.close_camera) 
        
        #设置为模板
        self.connect(self.setTmplAction,    SIGNAL("triggered()"),      self.set_as_tmpl)
        #开始工作按钮
        self.connect(self.start_action,     SIGNAL('triggered()'),      self.start_work)
        
        #鼠标的右键
        self.customContextMenuRequested.connect(self.showMenu)
        
        #启动定时器更新
        self.ctimer = QtCore.QTimer()        
        #将定时器与一个更新函数相连，这样可以时时更新界面 ,只要ctimer启动了就可以捕获图像 
        QtCore.QObject.connect(self.ctimer, QtCore.SIGNAL("timeout()"), self.update_by_video)
        
        #添加右键时的菜单,先初始化
        self.context_menu = None
        
        #保存模板事件
        self.connect(self.save_tm_action,     SIGNAL('triggered()'),      self.save_tm)
        #打开模板
        self.connect(self.open_tmpl_action,     SIGNAL('triggered()'),      self.open_tm)
        
    def init_gui(self):
        "开始画界面,也就是要先初始化好模板 "
        
        #先把初始化界面所需要的参数都赋上值
        self.camera_index = 0 #已经在用的摄像头编号 
        #先测试摄像头是不是能打开，不能的话直接转到以图片的方式来更新gui
        self.cap = cv2.VideoCapture(self.camera_index)
        
        self.tm = None
        self.init_from_myown_tmpl()
        
        '''                
        #第1种 ：从一个给定的图片
        if init_from == 'path':
            #imgurl = get_resource(init_img_name)
            imgurl = init_img_name
            self.init_from_imgpath(imgurl)
            #从图片打开的话，就需要把摄像头先关闭
            if self.cap.isOpened():
                self.cap.release()
                self.updating = 'no'
        
        #第二种：生产上用时得直接从摄像头取图片
        else:
            try:
                #如果没有打开
                if not self.cap.isOpened():
                    #从图片打开
                    self.init_from_imgpath(imgurl)
                    self.updating = 'no'
                else:
                    self.init_from_camera()
            except:
                self.init_from_imgpath(imgurl)
                self.updating = 'no'
        '''
        if self.cap.isOpened():
            self.cap.release()
            #记录界面是不是在用摄像头更新
            self.updating = 'no'
             

    def init_from_imgpath(self, imgpath):
        "默认打开一个图片来初始化界面作为模板"
        self.path = imgpath
        self.tm = Auto_tm(imgpath=imgpath)
        self.update()
        
        
    def init_from_myown_tmpl(self):
        "打开的应该是一个样本，而不是模板"
        imgsrc = np.zeros((400,1000,3), np.uint8)
        imgsrc = cv2.bitwise_not(imgsrc)        
        self.sample_frame = Sample(imgsrc, isvideo=False, th=self.paper_threshold).imgsrc
        
        #self.on_draw(self.sample_frame.get_res(self.tm))
        self.on_draw(self.sample_frame)
        
        
    def init_from_camera(self):
        '''从摄像头捕获图像
        '（可能会多次点击，如果未打开，操作就是先打开，如果已打开，那就拍照）'''
        
        #如果未打开，那操作只是打开而已
        if not self.cap.isOpened():
            #其实不需要设置模板的
            self.tm = Manual_tm(800,600) 
            res = self.open_camera()
            if res == -1:
                msg = '摄像头打开失败，请检查是否安装好！'
                alert(self, '错误', msg)
                return
        
        '''
        #如果已经打开，那就直接用
        elif:
            #1.截取当前一针的画面
            ret, self.curr_frame = self.cap.read()
            self.updating = 'no'
            
            #2.先停掉定时器
            self.ctimer.stop()
            #cv2.imwrite('E:/2kkkkk/a/9999.jpg', self.curr_frame)
            
            #3.也可以不用关闭摄像头
            #self.cap.release()'''
          
            
    def open_camera(self):
        "打开摄像头"
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            self.updating = 'yes'
            self.ctimer.start(freq)
        except Exception,e:
            alert(self, '发生异常', '异常信息 ：'+str(e))  
        
        if not self.cap.isOpened():
            alert(self, '提示', '摄像头打开失败！\n请确认已经安装好摄像头!')
            return -1
        else:
            return 0
    
    
    def close_camera(self):
        "关闭摄像头，一并关掉计时器"
        self.updating = 'no'
        if self.cap.isOpened():
            self.ctimer.stop()
            self.cap.release()
        

    def switch_camra(self):
        "切换摄像头，默认最多三个摄像头"
        #如果未打开，那就直接用
        if not self.cap.isOpened():
            self.open_camera()
            return
        
        if self.cap.isOpened():
            self.close_camera()
            
            #让摄像头在0 1 2之间循环
            if self.camera_index == 2:
                self.camera_index = 0
            else:
                self.camera_index += 1
            
            self.open_camera()
            return 
        
        
    def update_by_video(self):
        "捕获视频来更新界面 ,只能有这一个计时器，不然会有冲突的"
        _, self.sample_frame = self.cap.read()
        
        #如果已经设置了模板，那就需要把视频和模板实时比较
        if self.tm != None:
            self.on_draw(Sample(self.sample_frame).get_res(self.tm))
        else:
            self.on_draw(self.sample_frame)            
        
        #sample1 = Sample(cv2.imread('img/template_altered.png'))  #先模拟只有一张图片的情况
        #self.on_draw(sample1.get_res(self.tm))
        
        
    def set_as_tmpl(self):
        "设置成模板,将当前的sample_frame设置为tm"
        if self.sample_frame != None:
            self.tm = Auto_tm(img=self.sample_frame)

        alert(self, '消息', '模板设置成功！')     

        
    def start_work(self):
        "摄像头开始工作否开始不工作"
        #先判断是不是已经选中了'开始工作'
        if self.start_action.isChecked():
            #1.如果还没有设置模板
            if self.tm == None:
                alert(self, '消息', '请先设置模板！方法：调整好模板后，或直接打开一个模板，\n然后点击“设为模板”按钮!')
                self.start_action.setChecked(False)
                return                
            
            if self.tm == None:
                #if confirm(self, '确认', '是否将当前设置为模板？') != 'yes':
                alert(self, '消息', '请先设置模板！方法：调整好模板后，或直接打开一个模板，\n然后点击“设为模板”按钮!')
                self.start_action.setChecked(False)
                return
            else:
                self.start_action.setChecked(True)
            
            #------已有模板，直接开始匹配工作-------
            
            #1.打开摄像头
            res = self.open_camera()
            if res == -1:
                self.start_action.setChecked(False)
                return
            
            #2.直接打开计时器, 开始与模板匹配得出差异
            if self.updating != 'yes':
                self.ctimer.start(freq)
                self.updating = 'yes'
                         
        #手动不让它工作
        else:
            self.close_camera()
            

    def capture_action(self):
        "如果已打开，那就拍照,"
        
        #将当前的样本与模板相比较 
        
        
        
        ''' 
        #scene1:已经打开了摄像头
        if self.cap.isOpened():
            if self.updating == 'no':
                self.ctimer.start(freq)
                self.updating = 'yes'
            else:
                #1.截取当前一针的画面
                ret, self.curr_frame = self.cap.read()
                self.updating = 'no'
                
                #2.先停掉定时器
                self.ctimer.stop()
                #cv2.imwrite('E:/2kkkkk/a/9999.jpg', self.curr_frame)
                
                #3.也可以不用关闭摄像头
                #self.cap.release()  
                
                             
        #scene2：未用摄像头,当前已经在界面上显示的是静态图片
        else:
            self.init_from_camera()'''

           
    
    def set_manual_tm(self, w,h):
        """设置成手工创建的模板，传入的两个浮点数"""
        self.tm = Manual_tm(int(w), int(h))
    

    def update(self):
        '''更新画布'''
        self.on_draw(self.tm.get_tmpl())


    #重新画图
    def on_draw(self, data):
        
        h,w,_ = self.sample_frame.shape
             
        self.fig.clear()
        self.axes = self.fig.add_subplot(111, axisbg='r')
        
        #设置网格
        self.axes.grid(b='on') #, which='major', axis='both',color='gray', linestyle='..', linewidth=1

        #设置标记
        #x轴 都是间隔20毫米
        unit1 = 20
        xticks = np.arange(0, w, unit1)
        self.axes.set_xticks(xticks)
        xlabels = [a*unit1 for a in range(xticks.size)]
        #自定义x轴的标签
        xls = []
        for i in range(len(xlabels)):
            if (i+1)%3 == 0:
                xls.append(str(xlabels[i]))
            else:
                xls.append(' ')        
        self.axes.set_xticklabels(xls)
                
        yticks = np.arange(0, h, unit1)
        self.axes.set_yticks(yticks)
        ylabels = [a*unit1 for a in range(yticks.size)]
        #自定义y轴的标签
        yls = []
        for i in range(len(ylabels)):
            if (i+1)%3 == 0:
                yls.append(str(ylabels[i]))
            else:
                yls.append(' ')
        self.axes.set_yticklabels(yls)        

        #单位等标注  
        #self.axes.set_xlabel(r'$\Delta_i$', fontsize=20)
        self.axes.set_xlabel(r'mm', fontsize=15)
        self.axes.set_ylabel(r'mm', fontsize=15)
        #self.axes.set_title('Volume and percent change')                

        self.axes.imshow(data, interpolation='nearest')
        self.canvas.draw()
  
    
    def onclick(self,event):
        '点击界面时选择一个元素的操作'
        #print '按下鼠标键的编号:', event.button #按下鼠标键的编号
        #如果是点的右键，就直接返回，把处理的事件给别的人处理
        if event.button > 1:
            #如果是右键就弹出菜单
            return

        #图像画布上面的坐标，实际用到的坐标
        if event.xdata and event.ydata:
            xpos = int(event.xdata)
            ypos = int(event.ydata)
            #print '画布中的坐标:', xpos, ypos
        else:
            return 
        
        if self.tm:
            #找出点击了哪一个矩形元素，并更新选中的列表
            self.tm.find_out_rect_by_point((xpos, ypos))     
            #更新界面 
            self.update()
        else:
            print '未初始化模板'   
        

    def showMenu(self, pos):
        "点击右键时弹出一个小菜单"
        #由于有工具栏和菜单栏，所以需要把位置改变一下
        #print pos.x(), pos.y()
        pos = QPoint(pos.x()+8, pos.y()+78)
        
        #初始化右键菜单 
        if self.context_menu == None:
            self.context_menu = QMenu(self)
            
            self.change_dir_action = self.context_menu.addAction(u'切换放置方向')
            self.change_dir_action.triggered.connect(self.change_dir)
            
            self.up_down_action = self.context_menu.addAction(u"设置上下移动")
            self.up_down_action.triggered.connect(self.up_down)
            
            self.left_right_action = self.context_menu.addAction(u"设置左右移动")
            self.left_right_action.triggered.connect(self.left_right)            
            
        self.context_menu.popup(self.mapToGlobal(pos))        
    
    
    def change_dir(self):
        "把水平方向的换成竖直方向，或反过来 x,y,w,h"
        self.tm.change_element_dir()
        self.update() 
    
      
    def create_tmpl(self):
        self.set_paper_Dialog.show()
        
    def global_set(self):
        self.setting_Dialog.show()
    
    def add_element(self):
        self.add_element_Dialog.show()
        
    def remove_element(self):
        "去除选中的元素"
        if confirm(self, '消息', '你确定要移除已选中的元素吗？') == 'yes':
            self.tm.rm_element()
            self.update()


    def on_key_press(self, event):
        ''' #http://matplotlib.org/users/navigation_toolbar.html#navigation-keyboard-shortcuts
            #实现方向键的功能
        '''
        # implement the default mpl key press events described at
        #key_press_handler(event, self.canvas, self.mpl_toolbar)
        if str(event.key) == 'right':
            self.right_moved()
        elif str(event.key) == 'left':
            self.left_moved() 
        elif str(event.key) == 'up':
            self.up_moved()
        elif str(event.key) == 'down':
            self.down_moved()

    def right_moved(self,dis=0):
        self.tm.move_elements('r', 1, dis)
        self.update()
        
    def left_moved(self,dis=0):
        self.tm.move_elements('r', -1, dis)
        self.update()
    
    def up_moved(self,dis=0):
        self.tm.move_elements('d', -1, dis)
        self.update()
        
    def down_moved(self,dis=0):
        self.tm.move_elements('d', 1, dis)
        self.update()
    
    def up_down(self):
        "上下移动"
        text, ok = QtGui.QInputDialog.getText(self, \
                                              _fromUtf8('上下移动'),\
                                              _fromUtf8('请输入向上移动的距离(负数表示反向):'))
        dist = str(text).strip()
        if ok and dist:
            try:
                dist = float(dist)
                if dist >= 0: #大于0向上移动
                    self.up_moved( abs(int(dist)) )
                else:
                    self.down_moved( abs(int(dist)) )
                    
            except Exception,e:
                alert(self, '错误提醒', '设置错误：%s' % str(e))
                
        
    def left_right(self):
        "左右移动"
        text, ok = QtGui.QInputDialog.getText(self, \
                                              _fromUtf8('左右移动'),\
                                              _fromUtf8('请输入向右移动的距离(负数表示反向):'))
        dist = str(text).strip()
        if ok and dist:
            try:
                dist = float(dist)
                if dist >= 0: #大于0向上移动
                    self.right_moved( abs(int(dist)) )
                else:
                    self.left_moved( abs(int(dist)) )
                    
            except Exception,e:
                alert(self, '错误提醒', '设置错误：%s' % str(e))       
        
        
        
    def save_tm(self):
        "保存当前的模板" 
        text, ok = QtGui.QInputDialog.getText(self, \
                                              _fromUtf8('保存模板名称'),\
                                              _fromUtf8('请输入模板名称:'))
        name = str(text).strip()
        if ok and name:
            name = unicode(name,'utf8')#.encode('utf8')
            fname = os.path.join(unicode(get_relative_dir()), name)
            
            #默认以txt文件保存
            if not fname.endswith('.txt'):
                fname += u'.txt'
            f = open(fname,'w')
            tm = self.tm
            
            f.write('wh:'+str(tm.w)+' '+str(tm.h) + '\n')
            
            #将当前的设置的模板长宽与每个矩形的大小位置保存起来
            if self.tm:
                for e in tm.ele_list:
                    #先只画出没有选中的
                    x,y,w,h = e.x, e.y, e.w, e.h
                    #cv2.rectangle(bg, (x,y), (x+w,y+h), (86,170,255), -1)
                    f.write('rec:'+ str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + '\n')          


            f.close()
            
            alert(self, '保存模板', '模板已经保存成功！位置在:' + fname)
        else:
            pass 
                 
        
    def open_tm(self):
        "open模板"
        fname = QtGui.QFileDialog.getOpenFileName(self, _fromUtf8('打开模板'), get_relative_dir())
        if fname:
            self.filename = fname
            f = open(fname, 'r')
            ele_list = []
            
            lines = f.readlines()
            for line in lines:        
                if line:   
                    if line.startswith('wh:'):
                        wh = line[3:].split()
                        self.tm = Manual_tm(int(wh[0]), int(wh[1]))
                    if line.startswith('rec:'):
                        prop = line[4:].split()
                        #文件中是这样的顺序x,y,w,h
                        ele_w,ele_h, x,y = int(prop[2]),int(prop[3]),int(prop[0]),int(prop[1])
                        ele = Element('barcode', ele_w,ele_h, x,y)
                        ele_list.append(ele)
                        
            #循环完成后更新 模板中的图
            self.tm.add_elements(ele_list)
            #添加完成后更新界面
            self.update()           
                        
            
            
  
#if __name__ == "__main__":
app = QApplication(sys.argv)
ui = new_main_window()
ui.show()
sys.exit(app.exec_())
        
        
        
