#coding:utf8
'''
常用的一些函数
'''
import os,sys
from math import sqrt,ceil,fabs
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
from PyQt4 import QtCore

from globals import dpi


def _getpxs(f):
    #从浮点数转换成像素的大小
    return int(ceil(f/25.4*dpi))

def _calc(self,x):
    "计算转换成像素后的大小 "
    #return int(round(self.factor * x))


_fromUtf8 = None
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


def alert(parent, title, body):
    #界面上用于提示消息
    QMessageBox.about(parent, _fromUtf8(title), _fromUtf8(body))


def confirm(parent, title, body):
    "确认消息"
    title = _fromUtf8(title)
    body  = _fromUtf8(body)
    
    reply = QtGui.QMessageBox.question(parent, 
                                       title, 
                                       body, 
                                       QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, 
                                       QtGui.QMessageBox.No)

    if reply == QtGui.QMessageBox.Yes:
        return 'yes'
    else:
        return 'no' 

def get_resource(s):
    "返回图片等文件的全路径，s表示的是相对utils的相对路径，比如 img/img.jpg"
    cur_path = os.path.dirname(__file__)
    src_path = os.path.join(cur_path, s)
    #print os.path.exists(img_path)
    return src_path


def get_relative_dir():
    "获取的是只在一些模板或软件需要的信息的目录"
    cur_path = os.path.abspath(os.path.dirname(__file__))
    '''
    if 'ribo' in cur_path:
        cur_path = cur_path[:cur_path.index('ribo')+4]
    '''
    if cur_path.lower().startswith(('c:','d:','e:','f:','g:')):
        data_path = os.path.join(cur_path, 'ribodata')
    else:
        data_path = 'c:/ribodata'
        
    if not os.path.exists(data_path):
        print '不存在，创建新目录 '
        os.mkdir(data_path)
        
    return data_path
    


if __name__ == '__main__':
    #print get_resource('img/img_1931_s.jpg')
    print get_relative_dir()
    pass




