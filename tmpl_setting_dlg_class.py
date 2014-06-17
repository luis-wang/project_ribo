#coding:utf8
'''

'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
from PyQt4 import QtCore

import set_paper
from globals import dpi
from myutils import _fromUtf8,alert


class set_paper_Dialog(QDialog, set_paper.Ui_Dialog):
    """
    #设置纸张的大小 
    """    
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mainwin = parent
        #要以这种方式才会只调用一次
        self.connect(self.pushButton,   SIGNAL("clicked()"), self.clicked)
        #'currentIndexChanged(const QString&)'
        self.connect(self.comboBox,     SIGNAL("currentIndexChanged(QString)"), self.changed)
    
    def changed(self):
        """选择了标准大小就把自定义的input设置为空"""
        index = self.comboBox.currentIndex()
        #选择了一个标准值
        if index >0:
            self.custom_w_Edit.setText('')
            self.custom_h_Edit.setText('')
             
             
    #这里是根据on_XX_clicked这种方式来定义的事件
    def clicked(self):
        #根据这里选择的一个值来设置背景
        
        #这里是用来改变父窗口里的内容 
        #self.mainwin.showButton.setText("accept button")
        
        index = self.comboBox.currentIndex()
        total = self.comboBox.count()
        
        comb_text = str(self.comboBox.currentText())
        
        custom_w = str(self.custom_w_Edit.text())
        custom_h = str(self.custom_h_Edit.text())
        
        #print 'custom_w:custom_h',custom_w,custom_h
        if custom_w != '' and custom_h != '':
            try:
                w,h = float(custom_w),float(custom_h)
            except ValueError:
                alert(self, '错误数据','长和宽必须为小数或整数.')
                return
            
            if w<=0 or h<=0:
                #设置错误
                alert(self, '错误数据','不能是0或负数.')
                return
        
        #如果选择的是第一个，那就没有选择标准大小
        elif index == 0 :
            #当未选择标准大小，而且也没有设置两个自定义值时
            if custom_w == '' and custom_h == '':
                alert(self, '设置错误','请设置纸张的长和宽.')
                return

        #选择了标准大小中的一个        
        else:
            w,h = str(comb_text).split('x')
            

        #先将主窗口中的模板类转换成手工类Manual_tm
        self.mainwin.set_manual_tm(float(w),float(h))

        self.mainwin.update_tmpl()        
        self.close()
        




