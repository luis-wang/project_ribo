#coding:utf8
#!/usr/bin/env python
# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

'''
forked from makepyqt.pyw
'''


import os
import platform
import stat
import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
from PyQt4 import QtCore
from opencv_proc import *
from carve_new import Ui_MainWindow
from cvimage2 import CVImage,Tmpl_CVImage

from configdialog.configdialog import ConfigDialog

from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)


QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

__version__ = "1.2.5"

Windows = sys.platform.lower().startswith(("win", "microsoft"))



class OptionsForm(QDialog):

    def __init__(self, parent=None):
        super(OptionsForm, self).__init__(parent)

        settings = QSettings()
        if sys.platform.startswith("darwin"):
            pyuic4Label = QLabel("pyuic4 (pyuic.py)")
        else:
            pyuic4Label = QLabel("pyuic4")
        self.pyuic4Label = QLabel(settings.value("pyuic4",
                QVariant(PYUIC4)).toString())
        self.pyuic4Label.setFrameStyle(QFrame.StyledPanel|
                                       QFrame.Sunken)
        pyuic4Button = QPushButton("py&uic4...")
        pyrcc4Label = QLabel("pyrcc4")
        self.pyrcc4Label = QLabel(settings.value("pyrcc4",
                QVariant(PYRCC4)).toString())
        self.pyrcc4Label.setFrameStyle(QFrame.StyledPanel|
                                       QFrame.Sunken)
        pyrcc4Button = QPushButton("p&yrcc4...")
        pylupdate4Label = QLabel("pylupdate4")
        self.pylupdate4Label = QLabel(settings.value("pylupdate4",
                QVariant(PYLUPDATE4)).toString())
        self.pylupdate4Label.setFrameStyle(QFrame.StyledPanel|
                                           QFrame.Sunken)
        pylupdate4Button = QPushButton("&pylupdate4...")
        lreleaseLabel = QLabel("lrelease")
        self.lreleaseLabel = QLabel(settings.value("lrelease",
                QVariant("lrelease")).toString())
        self.lreleaseLabel.setFrameStyle(QFrame.StyledPanel|
                                         QFrame.Sunken)
        lreleaseButton = QPushButton("&lrelease...")
        toolPathGroupBox = QGroupBox("Tool Paths")

        pathsLayout = QGridLayout()
        pathsLayout.addWidget(pyuic4Label, 0, 0)
        pathsLayout.addWidget(self.pyuic4Label, 0, 1)
        pathsLayout.addWidget(pyuic4Button, 0, 2)
        pathsLayout.addWidget(pyrcc4Label, 1, 0)
        pathsLayout.addWidget(self.pyrcc4Label, 1, 1)
        pathsLayout.addWidget(pyrcc4Button, 1, 2)
        pathsLayout.addWidget(pylupdate4Label, 2, 0)
        pathsLayout.addWidget(self.pylupdate4Label, 2, 1)
        pathsLayout.addWidget(pylupdate4Button, 2, 2)
        pathsLayout.addWidget(lreleaseLabel, 3, 0)
        pathsLayout.addWidget(self.lreleaseLabel, 3, 1)
        pathsLayout.addWidget(lreleaseButton, 3, 2)
        toolPathGroupBox.setLayout(pathsLayout)

        resourceModuleNamesGroupBox = QGroupBox(
                "Resource Module Names")
        qrcFiles = bool(int(settings.value("qrc_resources", "1").toString()))
        self.qrcRadioButton = QRadioButton("&qrc_file.py")
        self.qrcRadioButton.setChecked(qrcFiles)
        self.rcRadioButton = QRadioButton("file_&rc.py")
        self.rcRadioButton.setChecked(not qrcFiles)

        radioLayout = QHBoxLayout()
        radioLayout.addWidget(self.qrcRadioButton)
        radioLayout.addWidget(self.rcRadioButton)
        resourceModuleNamesGroupBox.setLayout(radioLayout)

        self.pyuic4xCheckBox = QCheckBox("Run pyuic4 with -&x "
                " to make forms stand-alone runable")
        x = bool(int(settings.value("pyuic4x", "0").toString()))
        self.pyuic4xCheckBox.setChecked(x)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                     QDialogButtonBox.Cancel)

        layout = QVBoxLayout()
        layout.addWidget(toolPathGroupBox)
        layout.addWidget(resourceModuleNamesGroupBox)
        layout.addWidget(self.pyuic4xCheckBox)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(pyuic4Button, SIGNAL("clicked()"),
                lambda: self.setPath("pyuic4"))
        self.connect(pyrcc4Button, SIGNAL("clicked()"),
                lambda: self.setPath("pyrcc4"))
        self.connect(pylupdate4Button, SIGNAL("clicked()"),
                lambda: self.setPath("pylupdate4"))
        self.connect(lreleaseButton, SIGNAL("clicked()"),
                lambda: self.setPath("lrelease"))
        self.connect(buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(buttonBox, SIGNAL("rejected()"), self.reject)

        self.setWindowTitle("Make PyQt - Options")
   


    def accept(self):
        settings = QSettings()
        settings.setValue("pyuic4", QVariant(self.pyuic4Label.text()))
        settings.setValue("pyrcc4", QVariant(self.pyrcc4Label.text()))
        settings.setValue("pylupdate4",
                QVariant(self.pylupdate4Label.text()))
        settings.setValue("lrelease", QVariant(self.lreleaseLabel.text()))
        settings.setValue("qrc_resources",
                "1" if self.qrcRadioButton.isChecked() else "0")
        settings.setValue("pyuic4x",
                "1" if self.pyuic4xCheckBox.isChecked() else "0")
        QDialog.accept(self)


    def setPath(self, tool):
        if tool == "pyuic4":
            label = self.pyuic4Label
        elif tool == "pyrcc4":
            label = self.pyrcc4Label
        elif tool == "pylupdate4":
            label = self.pylupdate4Label
        elif tool == "lrelease":
            label = self.lreleaseLabel
        path = QFileDialog.getOpenFileName(self,
                "Make PyQt - Set Tool Path", label.text())
        if path:
            label.setText(QDir.toNativeSeparators(path))





        



class Form(QMainWindow):
    """
    "操作的主窗口
    """

    def __init__(self):
        super(Form, self).__init__(None)
        #self.resize(800, 400)  #把主窗口设置成这样大
        self.showMaximized() #最大化
        
        #用于保存内存显示的图片
        self.image = QImage()
        
        #保存已经选择上的矩形
        self.selected_rects = []

        pathLabel = QLabel(_fromUtf8("图像路径:"))
        settings = QSettings()
        rememberPath = settings.value("rememberpath", QVariant(True if Windows else False)).toBool()
                
        if rememberPath:
            path = (unicode(settings.value("path").toString()) or os.getcwd())
        else:
            path = (sys.argv[1] if len(sys.argv) > 1 and
                    QFile.exists(sys.argv[1]) else os.getcwd())
            
        path = 'img/img_1931_s.jpg'
            
        self.pathLabel = QLabel(path)
        self.pathLabel.setFrameStyle(QFrame.StyledPanel| QFrame.Sunken)
        
        self.pathLabel.setToolTip(_fromUtf8("可以从这里直接打开图片分析！"))
        self.pathButton = QPushButton(_fromUtf8("打开.."))
        self.captureBtn = QPushButton(_fromUtf8('拍照'))
        
        self.imageLabel = QLabel('')

        self.upBtn = QPushButton(_fromUtf8('上'))
        self.upBtn.setMaximumSize(QtCore.QSize(30, 16777215))
        
        self.downBtn = QPushButton(_fromUtf8('下'))
        self.downBtn.setMaximumSize(QtCore.QSize(30, 16777215))        

        self.leftBtn = QPushButton(_fromUtf8('左'))
        self.leftBtn.setMaximumSize(QtCore.QSize(30, 16777215))

        self.leftBtn = QPushButton(_fromUtf8('左'))
        self.leftBtn.setMaximumSize(QtCore.QSize(30, 16777215))
        
        self.rightBtn = QPushButton(_fromUtf8('右'))
        self.rightBtn.setMaximumSize(QtCore.QSize(30, 16777215))
        
        self.distEdit = QtGui.QLineEdit('10')
        self.rightBtn.setMaximumSize(QtCore.QSize(40, 16777215))
        
        self.distUnit = QLabel(_fromUtf8('毫米'))
        self.distUnit.setMaximumSize(QtCore.QSize(40, 16777215))
        
        self.recurseCheckBox = QCheckBox("&Recurse")

        self.transCheckBox = QCheckBox("&Translate")

        self.debugCheckBox = QCheckBox("&Dry Run")
        
        
        
        self.buttonBox = QDialogButtonBox()
        menu = QMenu(self)
        setTmplAction = menu.addAction(_fromUtf8('设置模板'))
        optionsAction = menu.addAction("&Options...")
        self.rememberPathAction = menu.addAction("&Remember path")
        self.rememberPathAction.setCheckable(True)
        self.rememberPathAction.setChecked(rememberPath)
        aboutAction = menu.addAction(_fromUtf8('关于'))
        moreButton = self.buttonBox.addButton(_fromUtf8('更多'),
                QDialogButtonBox.ActionRole)
        moreButton.setMenu(menu)

        #self.buildButton = self.buttonBox.addButton("&Build",QDialogButtonBox.ActionRole)

        #self.cleanButton = self.buttonBox.addButton("&Clean", QDialogButtonBox.ActionRole)
        self.cleanButton = self.buttonBox.addButton(_fromUtf8('设为模板'), QDialogButtonBox.ActionRole)
        
        self.cleanButton.setToolTip(_fromUtf8('将导入的图片，或经过修改的图片设置为模板，检测时将用此作为位置标准'))
        
        
        quitButton = self.buttonBox.addButton(_fromUtf8("退出"), QDialogButtonBox.RejectRole)

        topLayout = QHBoxLayout()
        topLayout.addWidget(pathLabel)
        topLayout.addWidget(self.pathLabel, 1)
        topLayout.addWidget(self.pathButton)
        topLayout.addWidget(self.captureBtn)
              
        #底栏的操作按钮
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.upBtn)
        bottomLayout.addWidget(self.downBtn)
        bottomLayout.addWidget(self.leftBtn)
        bottomLayout.addWidget(self.rightBtn)
        bottomLayout.addWidget(self.distEdit)
        bottomLayout.addWidget(self.distUnit)
        
        bottomLayout.addWidget(self.recurseCheckBox)
        bottomLayout.addWidget(self.transCheckBox)
        bottomLayout.addWidget(self.debugCheckBox)
        bottomLayout.addStretch()
        bottomLayout.addWidget(self.buttonBox)

        layout = QVBoxLayout()
        layout.addLayout(topLayout)
        
        
        
        #初始化载入的图像 
        self.main_frame = QWidget()

        self.fig = Figure((10.0, 5.0 ), dpi=72) #这里不知道怎么设置好
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()
        

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        self.canvas.mpl_connect('key_press_event', self.on_key_press) 
        self.canvas.mpl_connect('button_press_event', self.onclick)
        
        
        #layout.addWidget(self.imageLabel)
        layout.addWidget(self.canvas)
        #layout.addWidget(self.mpl_toolbar)
        

        layout.addLayout(bottomLayout)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        #self.ad

        self.connect(aboutAction,       SIGNAL("triggered()"),      self.about)
        self.connect(optionsAction,     SIGNAL("triggered()"),      self.setOptions)
        self.connect(setTmplAction,     SIGNAL("triggered()"),      self.setTmplAction)
        self.connect(self.pathButton,   SIGNAL("clicked()"),        self.setPath)
        #self.connect(self.buildButton, SIGNAL("clicked()"),        self.build)
        self.connect(self.cleanButton,  SIGNAL("clicked()"),        self.set_as_tmpl)
        self.connect(quitButton,        SIGNAL("clicked()"),        self.close)

        self.setWindowTitle(_fromUtf8("图像操作窗"))
        
        #--------------------------------------------------------#
        
        #初始化一个图片
        self.loadImage()
        
        #生产上用时得直接从摄像头取图片
        #self.captureImage()
        
        #初始化小的对话框
        self.init_dialogs()
        
        self.custom_slots()
        
        
    def init_dialogs(self):
        #设置纸张
        from dlg_classes import set_paper_Dialog
        self.set_paper_Dialog = set_paper_Dialog(self)
        
        
    def custom_slots(self):
        """
        "自定义一些事件
        """
        self.captureBtn.clicked.connect(self.captureImg)
        
        #方向键的使用
        self.upBtn.clicked.connect(self.up_moved)
        self.rightBtn.clicked.connect(self.right_moved)
        self.downBtn.clicked.connect(self.down_moved)
        self.leftBtn.clicked.connect(self.left_moved)        
    
        
    def on_draw(self,data):     
        self.fig.clear()
        
        #self.axes = self.fig.add_subplot(111) # = (1,1,1)
        self.axes = self.fig.add_subplot(111, axisbg='r')
        '''
        import matplotlib.gridspec as gridspec
        gs = gridspec.GridSpec(2, 2,
                               width_ratios=[1,2],
                               height_ratios=[4,1]
                               )
        
        ax1 = plt.subplot(gs[0])        
        '''
        #self.axes = self.fig.add_subplot(111)
        
        #设置网格
        self.axes.grid(True)
        #ax.yaxis.grid(True)
        
        #self.axes.plot(self.x, self.y, 'ro')
        
        self.axes.imshow(data, interpolation='nearest')
        #self.axes.plot([1,2,3])
        self.canvas.draw()
        
      
        
    def captureImage(self):
        self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened():
            print '摄像头已经打开了'
        else:
            #cap.open()
            print '摄像头未打开！'
                 
        # Paint every 50 ms
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update_label_image)
        self._timer.start(50)
    
    
    def on_key_press(self, event):
        print('you pressed', event.key)
        # implement the default mpl key press events described at
        # http://matplotlib.org/users/navigation_toolbar.html#navigation-keyboard-shortcuts
        key_press_handler(event, self.canvas, self.mpl_toolbar)

            
    def onclick(self,event):
        print event.button #按下鼠标键的编号
        print '整个窗口的坐标：',event.x, event.y
        
        #图像画布上面的坐标，实际用到的坐标
        if event.xdata and event.ydata:
            xpos = int(event.xdata)
            ypos = int(event.ydata)
            print '画布中的坐标:', xpos, ypos
        else:
            return 
           
        #返回是不是点击了某个矩形，如果有就返回一个dict的name
        rectname = self.cv_image.find_out_rect_by_point((xpos,ypos))
        
        #至少点击到一个矩形
        if rectname:
            print '找到了一个矩形：',rectname
            
            if rectname in self.selected_rects:
                self.selected_rects.remove(rectname)
            else:
                self.selected_rects.append(rectname)
            print '已经选上的矩形:',self.selected_rects
            

            
            #找到后将所有选中的矩形用绿色标识出来
            self.data =  self.cv_image.draw_rects(self.selected_rects)
            self.on_draw(self.data)
            

        else:
            print '没有找到任何矩形！！！'            
            
            

    def loadImage(self):
        """
        "默认打开一个图片
        """
        
        #self.data = self.cv_image.res
        #self.on_draw(self.data)
        #操作图片类的所有信息
        self.cv_image = CVImage(str(self.pathLabel.text()))
        
        self.update_canvas()
        
    

    def update_canvas(self):
        self.data =  self.cv_image.draw_rects(self.selected_rects)
        self.on_draw(self.data)   
             
        
    #用opencv的图片更新成QImage的图像
    def update_Qimage(self, cvimg):
        #显示出上面处理后的结果
        height, width, bytesPerComponent = cvimg.shape
        bytesPerLine = 3 * width
        
        #转换成rgb格式   
        cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        self.image = QImage(cvimg.data, width, height, bytesPerLine, QImage.Format_RGB888)            
        self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
        
        #重新设置父组件的大小 
        #self.horizontalWidget.setGeometry(QtCore.QRect(0, 0, width, height))
        #self.imageLabel.resize(width, height)
        
    '''  
    def mousePressEvent(self, QMouseEvent):
        """
        "获取鼠标点击事件，并确定的位置,已经无用了
        """
        print '触发qt本身的事件......'
        
        
        #cursor = QtGui.QCursor(self)
        #position = QMouseEvent.pos()
        
        xpos = QMouseEvent.x()-10
        ypos = QMouseEvent.y()-50  #要考虑的是还有菜单栏的高度
        print 'xpos,ypos = ',xpos,ypos
        
        #返回点击事件处理后的结果，把相应的矩形标识出来
        rect = find_out_rect_by_point((xpos,ypos), self.cv_image.rects)
        
        #至少点击到一个矩形
        if rect:
            print '找到了一个矩形：',rect
            
            if rect in self.selected_rects:
                self.selected_rects.remove(rect)
            else:
                self.selected_rects.append(rect)
            print '已经选上的矩形:',self.selected_rects
            #找到后将所有选中的矩形用绿色标识出来
            self.cv_image.res = draw_rects(self.cv_image.red_blob, self.selected_rects)
            self.update_Qimage(self.cv_image.res)
            print '更新完成!!'
        else:
            print '没有找到任何矩形！！！'
    '''

    
    
    def calc_all_moved(self, dire, dis):
        """
        "每次移动，都重新计算所有的选中矩形各被移动了多少,向入移动的方向
        """
        
        if dire == 'r':
            d1 = {'l':0, 'r':dis, 'u':0, 'd':0}
        elif dire == 'l':
            d1 = {'l':dis, 'r':0, 'u':0, 'd':0}
        elif dire == 'u':
            d1 = {'l':0, 'r':0, 'u':dis, 'd':0}           
        elif dire == 'd':
            d1 = {'l':0, 'r':0, 'u':0, 'd':dis}
            
        #需要每次都更新选中的
        self.cv_image.set_new_rects(self.selected_rects, d1)
                    
        self.data =  self.cv_image.draw_rects(self.selected_rects)
        self.on_draw(self.data)                

        
    
    def right_moved(self):
        print '向右移动了!!!'
        
        #每一次都需要重新计算所有的位置
        dis = int(self.distEdit.text())
        self.calc_all_moved('r', dis)
        

    def left_moved(self):
        print '向左移动了!!!'
        
        #每一次都需要重新计算所有的位置
        dis = int(self.distEdit.text())
        self.calc_all_moved('l', dis)
    

    def up_moved(self):
        print '向上移动了!!!'
        
        #每一次都需要重新计算所有的位置
        dis = int(self.distEdit.text())
        self.calc_all_moved('u', dis) 
    

    def down_moved(self):
        print '向下移动了!!!'
        
        #每一次都需要重新计算所有的位置
        dis = int(self.distEdit.text())
        self.calc_all_moved('d', dis)  
            
    
    def captureImg(self):
        """
        "从视频中截取一张图像
        """
        print 'captureImg ...'
        if self._timer.isActive():
            #1.停止计时器
            self._timer.stop()
            print 'ok1,已经停止'

            #2.停止摄像头
            if self.cap.isOpened():
                self.cap.release()
                print '2release(ed)'
            #3.保存当前针            
            self.update_Qimage(self.cv_image.imgsrc)
            print '3ok'           

        else:
            print '未执行'

    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue("rememberpath",
                QVariant(self.rememberPathAction.isChecked()))
        settings.setValue("path", QVariant(self.pathLabel.text()))
        event.accept()


    def about(self):
        QMessageBox.about(self, "关于About Make PyQt",
                """<b>Make PyQt</b> v {0}
                <p>Copyright &copy; 2007-10 Qtrac Ltd. 
                All rights reserved.
                <p>This application can be used to build PyQt
                applications.
                It runs pyuic4, pyrcc4, pylupdate4, and lrelease as
                required, although pylupdate4 must be run directly to
                create the initial .ts files.
                <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
                __version__, platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR,
                platform.system()))


    def setPath(self):
        '''
        path = QFileDialog.getExistingDirectory(self,
                "Make PyQt - Set Path", self.pathLabel.text())
        if path:
            self.pathLabel.setText(QDir.toNativeSeparators(path))
        '''
        fname = QtGui.QFileDialog.getOpenFileName(self, '选择一张图片', 'img/')
        print 'fname:',fname
        if fname:
            self.pathLabel.setText(QDir.toNativeSeparators(fname))
            #更新ui
            fname = str(fname)
            #保存下来上次的模板
            tmpl_bg = self.cv_image.tmpl_bg
            tmpl_rects = self.cv_image.rect_list
            
            #设置新的载入图像 
            self.cv_image = CVImage(fname)
            self.cv_image.tmpl_bg = tmpl_bg
            self.cv_image.tmpl_rects = tmpl_rects
            
            #载入新图像需要重置选中的框
            self.selected_rects = []
            
            self.update_canvas()


    def setOptions(self):
        #dlg = OptionsForm(self)
        #dlg.exec_()
        #from set_paper import Ui_Dialog as Set_paper_dlg
        #set_paper_dlg = Set_paper_dlg(self)
        #set_paper_dlg.exec_()
        self.set_paper_Dialog.show()
        print '打开了'
        
        
    def setTmplAction(self):
        
        tmpl_dlg = ConfigDialog(self)
        tmpl_dlg.exec_()

        
    def set_w_h(self, w, h):
        print '长和宽已经重新设定：',w,h
        assert type(w) == type(h) == type(0)
        self.w, self.h = w,h 
        
        #重要绘制一个背景图片
        #把模板设置为当前的自身，然后就不变了
        self.cv_image.set_as_template()
        
        #更新ui
        self.data =  self.cv_image.draw_rects(self.selected_rects)
        self.on_draw(self.data)
        print '设置模板成功。。。'
        


    def build(self):
        self.updateUi(False)
        self.logBrowser.clear()
        recurse = self.recurseCheckBox.isChecked()
        path = unicode(self.pathLabel.text())
        self._apply(recurse, self._build, path)
        if self.transCheckBox.isChecked():
            self._apply(recurse, self._translate, path)
        self.updateUi(True)


    def set_as_tmpl(self):
        """
        self.updateUi(False)
        self.logBrowser.clear()
        recurse = self.recurseCheckBox.isChecked()
        path = unicode(self.pathLabel.text())
        self._apply(recurse, self._clean, path)
        self.updateUi(True)
        """
        '''
        '设置成一个模板，只需要把新的所有位置以蓝色的矩形画到背景上面就可以了
        '''

        
        reply = QtGui.QMessageBox.question(self, _fromUtf8('提醒'),
            _fromUtf8("是否设置成模板?"), QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        
        if reply == QtGui.QMessageBox.Yes:
            #把模板设置为当前的自身，然后就不变了
            self.cv_image.set_as_template()
            
            #更新ui
            self.data =  self.cv_image.draw_rects(self.selected_rects)
            self.on_draw(self.data)
            print '设置模板成功。。。'
        else:
            print '未设置'       
              
        
        


    def updateUi(self, enable):
        for widget in (self.buildButton, self.cleanButton,
                self.pathButton, self.recurseCheckBox,
                self.transCheckBox, self.debugCheckBox):
            widget.setEnabled(enable)
        if not enable:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        else:
            QApplication.restoreOverrideCursor()
            self.buildButton.setFocus()


    def _apply(self, recurse, function, path):
        if not recurse:
            function(path)
        else:
            for root, dirs, files in os.walk(path):
                for dir in sorted(dirs):
                    function(os.path.join(root, dir))


    def _make_error_message(self, command, process):
        err = ""
        ba = process.readAllStandardError()
        if not ba.isEmpty():
            err = ": " + str(QString(ba))
        return "<font color=red>FAILED: %s%s</font>" % (command, err)


    def _build(self, path):
        settings = QSettings()
        pyuic4 = unicode(settings.value("pyuic4",
                                        QVariant(PYUIC4)).toString())
        pyrcc4 = unicode(settings.value("pyrcc4",
                                        QVariant(PYRCC4)).toString())
        prefix = unicode(self.pathLabel.text())
        pyuic4x = bool(int(settings.value("pyuic4x", "0").toString()))
        if not prefix.endswith(os.sep):
            prefix += os.sep
        failed = 0
        process = QProcess()
        for name in os.listdir(path):
            source = os.path.join(path, name)
            target = None
            if source.endswith(".ui"):
                target = os.path.join(path,
                                    "ui_" + name.replace(".ui", ".py"))
                command = pyuic4
            elif source.endswith(".qrc"):
                if bool(int(settings.value("qrc_resources", "1").toString())):
                    target = os.path.join(path,
                                        "qrc_" + name.replace(".qrc", ".py"))
                else:
                    target = os.path.join(path, name.replace(".qrc", "_rc.py"))
                command = pyrcc4
            if target is not None:
                if not os.access(target, os.F_OK) or (
                   os.stat(source)[stat.ST_MTIME] >
                   os.stat(target)[stat.ST_MTIME]):
                    args = ["-o", target, source]
                    if command == PYUIC4 and pyuic4x:
                        args.insert(0, "-x")
                    if (sys.platform.startswith("darwin") and
                        command == PYUIC4):
                        command = sys.executable
                        args = [PYUIC4] + args
                    msg = ("converted <font color=darkblue>" + source +
                           "</font> to <font color=blue>" + target +
                           "</font>")
                    if self.debugCheckBox.isChecked():
                        msg = "<font color=green># " + msg + "</font>"
                    else:
                        process.start(command, args)
                        if (not process.waitForFinished(2 * 60 * 1000) or
                            not QFile.exists(target)):
                            msg = self._make_error_message(command,
                                                           process)
                            failed += 1
                    self.logBrowser.append(msg.replace(prefix, ""))
                else:
                    self.logBrowser.append("<font color=green>"
                            "# {0} is up-to-date</font>".format(
                            source.replace(prefix, "")))
                QApplication.processEvents()
        if failed:
            QMessageBox.information(self, "Make PyQt - Failures",
                    "Try manually setting the paths to the tools "
                    "using <b>More-&gt;Options</b>")


    def _clean(self, path):
        prefix = unicode(self.pathLabel.text())
        if not prefix.endswith(os.sep):
            prefix += os.sep
        deletelist = []
        for name in os.listdir(path):
            target = os.path.join(path, name)
            source = None
            if (target.endswith(".py") or target.endswith(".pyc") or
                target.endswith(".pyo")):
                if name.startswith("ui_") and not name[-1] in "oc":
                    source = os.path.join(path, name[3:-3] + ".ui")
                elif name.startswith("qrc_"):
                    if target[-1] in "oc":
                        source = os.path.join(path, name[4:-4] + ".qrc")
                    else:
                        source = os.path.join(path, name[4:-3] + ".qrc")
                elif name.endswith(("_rc.py", "_rc.pyo", "_rc.pyc")):
                    if target[-1] in "oc":
                        source = os.path.join(path, name[:-7] + ".qrc")
                    else:
                        source = os.path.join(path, name[:-6] + ".qrc")
                elif target[-1] in "oc":
                    source = target[:-1]
                if source is not None:
                    if os.access(source, os.F_OK):
                        if self.debugCheckBox.isChecked():
                            self.logBrowser.append("<font color=green>"
                                    "# delete {0}</font>".format(
                                    target.replace(prefix, "")))
                        else:
                            deletelist.append(target)
                    else:
                        self.logBrowser.append("<font color=darkred>"
                                "will not remove "
                                "'{0}' since `{1}' not found</font>"
                                .format(target.replace(prefix, ""),
                                source.replace(prefix, "")))
        if not self.debugCheckBox.isChecked():
            for target in deletelist:
                self.logBrowser.append("deleted "
                        "<font color=red>{0}</font>".format(
                        target.replace(prefix, "")))
                os.remove(target)
                QApplication.processEvents()


    def _translate(self, path):
        prefix = unicode(self.pathLabel.text())
        if not prefix.endswith(os.sep):
            prefix += os.sep
        files = []
        tsfiles = []
        for name in os.listdir(path):
            if name.endswith((".py", ".pyw")):
                files.append(os.path.join(path, name))
            elif name.endswith(".ts"):
                tsfiles.append(os.path.join(path, name))
        if not tsfiles:
            return
        settings = QSettings()
        pylupdate4 = unicode(settings.value("pylupdate4",
                             QVariant(PYLUPDATE4)).toString())
        lrelease = unicode(settings.value("lrelease",
                           QVariant(LRELEASE)).toString())
        process = QProcess()
        failed = 0
        for ts in tsfiles:
            qm = ts[:-3] + ".qm"
            command1 = pylupdate4
            args1 = files + ["-ts", ts]
            command2 = lrelease
            args2 = ["-silent", ts, "-qm", qm]
            msg = "updated <font color=blue>{0}</font>".format(
                    ts.replace(prefix, ""))
            if self.debugCheckBox.isChecked():
                msg = "<font color=green># {0}</font>".format(msg)
            else:
                process.start(command1, args1)
                if not process.waitForFinished(2 * 60 * 1000):
                    msg = self._make_error_message(command1, process)
                    failed += 1
            self.logBrowser.append(msg)
            msg = "generated <font color=blue>{0}</font>".format(
                    qm.replace(prefix, ""))
            if self.debugCheckBox.isChecked():
                msg = "<font color=green># {0}</font>".format(msg)
            else:
                process.start(command2, args2)
                if not process.waitForFinished(2 * 60 * 1000):
                    msg = self._make_error_message(command2, process)
                    failed += 1
            self.logBrowser.append(msg)
            QApplication.processEvents()
        if failed:
            QMessageBox.information(self, "Make PyQt - Failures",
                    "Try manually setting the paths to the tools "
                    "using <b>More-&gt;Options</b>")


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    PATH = unicode(app.applicationDirPath())
    print ('abc='+PATH)
    
    
    
    
    if Windows:
        PATH = os.path.join(os.path.dirname(sys.executable),
                            "Lib/site-packages/PyQt4")
        if os.access(os.path.join(PATH, "bin"), os.R_OK):
            PATH = os.path.join(PATH, "bin")
    if sys.platform.startswith("darwin"):
        i = PATH.find("Resources")
        if i > -1:
            PATH = PATH[:i] + "bin"
    PYUIC4 = os.path.join(PATH, "pyuic4")
    if sys.platform.startswith("darwin"):
        PYUIC4 = os.path.dirname(sys.executable)
        i = PYUIC4.find("Resources")
        if i > -1:
            PYUIC4 = PYUIC4[:i] + "Lib/python2.6/site-packages/PyQt4/uic/pyuic.py"
    PYRCC4 = os.path.join(PATH, "pyrcc4")
    PYLUPDATE4 = os.path.join(PATH, "pylupdate4")
    LRELEASE = "lrelease"
    if Windows:
        PYUIC4 = PYUIC4.replace("/", "\\") + ".bat"
        PYRCC4 = PYRCC4.replace("/", "\\") + ".exe"
        PYLUPDATE4 = PYLUPDATE4.replace("/", "\\") + ".exe"
        
        
        
        
        
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    app.setApplicationName("Make PyQt")
    if len(sys.argv) > 1 and sys.argv[1] == "-c":
        settings = QSettings()
        settings.setValue("pyuic4", QVariant(PYUIC4))
        settings.setValue("pyrcc4", QVariant(PYRCC4))
        settings.setValue("pylupdate4", QVariant(PYLUPDATE4))
        settings.setValue("lrelease", QVariant(LRELEASE))
    form = Form()
    form.show()
    app.exec_()

