#coding:utf8
'''

'''
import os
import platform
import stat
import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
from PyQt4 import QtCore
from cvimage2 import CVImage

from globals import dpi
from element import Element
from auto_tm import Auto_tm
from manual_tm import Manual_tm

import setting_dialog

from globals import dpi,move_dis
from myutils import _fromUtf8,alert

class setting_Dialog(QDialog, setting_dialog.Ui_Setting_Dialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.set_default_val()
        self.mainwin = parent
        self.connect(self.okButton,     SIGNAL('clicked()'),            self.submit)
        self.connect(self.paperSlider,  SIGNAL('valueChanged(int)'),    self.paperSlider_change)
        
    def set_default_val(self):
        "默认值 "
        self.lineEdit.setText(str(move_dis))
        #self.paperSlider.setValue()
        self.lineEdit_err_dis.setText('1.0')
    
    def paperSlider_change(self, value):
        self.pz = value
        print 'pz = ', self.pz
        
        if self.mainwin != None:
            self.mainwin.paper_threshold = self.pz
            print 'self.mainwin.paper_threshold = ',self.mainwin.paper_threshold 
    
    def submit(self):
        #判断每次移动的距离填写是不是正常
        try:
            dis = float(str(self.lineEdit.text()))
            err_dis = float(str(self.lineEdit_err_dis.text()))
        except ValueError:
            alert(self, '设置错误','距离值设置错误，应该是正的小数或整数.')
            return
        
        #把这个值保存到模板中去
        if self.mainwin.tm != None:
            self.mainwin.tm.dis = dis
            self.mainwin.tm.err_dis = err_dis
        
        self.close()
        
        
        
        
        
        
        
