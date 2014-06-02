#coding:utf8
'''

'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
from PyQt4 import QtCore

from element import Element
from manual_tm import Manual_tm
import add_element
from myutils import _fromUtf8,alert

    
class add_element_Dialog(QDialog, add_element.Ui_Dialog):
    """
    #添加元素的对话框
    """
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.mainwin = parent
        self.set_default_values()
        self.connect(self.pushButton, SIGNAL('clicked()'), self.submit)
        
    def set_default_values(self):
        #设置一些默认值 
        self.ele_type_comboBox.setCurrentIndex(1)
        self.ele_w_Edit.setText('40') #四十毫米
        self.ele_h_Edit.setText('15')
        
    def submit(self):
        ele_type_index = self.ele_type_comboBox.currentIndex()
        ele_type_text = str(self.ele_type_comboBox.currentText())
        
        if ele_type_index == 0:
            alert(self, '错误提醒', '请先选择一个元素类型.')
            return
        elif ele_type_index == 1:
            self.ele_type = 'barcode'
        elif ele_type_index == 2:
            self.ele_type = 'dimcode'
        
        try:
            #元素的尺寸 宽和高
            ele_w = float(str(self.ele_w_Edit.text()))
            ele_h = float(str(self.ele_h_Edit.text()))
            #print '宽和高：',ele_w,ele_h
            
            left_margin = float(str(self.left_margin_Edit.text()))
            top_margin = float(str(self.top_margin_Edit.text()))
                    
            row_num = int(str(self.row_num_Edit.text())) #行数
            col_num = int(str(self.col_num_Edit.text())) #列数
            h_space = float(str(self.h_space_Edit.text())) #水平间距
            v_space = float(str(self.v_space_Edit.text())) #垂直间距
        except ValueError:
            alert(self, '数值设置错误', '行数和列数应为整数，水平和垂直间距可为小数.')
            return
        
        
        #判断是不是已经设置了纸张大小 
        if isinstance(self.mainwin.tm, Manual_tm):
            if ele_w <=0 or ele_h <=0:
                alert(self, '数值设置错误', '元素的宽和高应该为大于0的小数或整数.')
                return
            if row_num <1 or col_num <1:
                alert(self, '数值设置错误', '行数和列数应该不小于1.')
                return
            self.construct_add_eles(ele_w,ele_h, left_margin,top_margin, 
                                    row_num, col_num, h_space, v_space)             
        else:
            alert(self, '提醒', '添加元素前请先设置纸张的长宽值.')
            return
        
        self.close()
        
        
    def construct_add_eles(self, ele_w,ele_h, left_margin,top_margin, 
                                 row_num, col_num, h_space, v_space):
        """
        "直接在添加时就构造出Element的元素，省得传来传去的
        "这里直接全部把毫米计算成像素
        """
        #只有row_num,col_num为整数，别的为浮点数
        
        #需要转换成相应的像素值
        #元素大小
        ###ele_w, ele_h = self._calc(ele_w), self._calc(ele_h)
        #距离左边和上边的距离
        ###left_margin,top_margin = self._calc(left_margin), self._calc(top_margin)
        #间距
        ###h_space,v_space = self._calc(h_space), self._calc(v_space)
        
        print '-------------------'
        print ele_w,ele_h, left_margin,top_margin, row_num,col_num,h_space,v_space
        print '-------------------'
        ele_w,ele_h = int(ele_w), int(ele_h)
        left_margin,top_margin = int(left_margin),int(top_margin)
        row_num,col_num = int(row_num),int(col_num)
        h_space,v_space = int(h_space),int(v_space)
        
        ele_list = []
        
        #一行一行地产生矩形，有多少列就有多少个行元素
        for c in range(col_num):
            for r in range(row_num):
                #内层循环中这一列列的元素，所以x值是相同的
                
                x = left_margin + c * (ele_w + h_space)
                y = top_margin +  r * (ele_h + v_space)
                
                #构造新元素
                ele = Element(self.ele_type, ele_w,ele_h, x,y)
                #gen_rects.append([x,y, ele_w,ele_h])
                ele_list.append(ele)
                
        '''
        for rec in gen_rects:
            x,y,w,h = rec
            cv2.rectangle(self.imgsrc,(x,y),(x+w,y+h),(0,0,255),2)
        '''
        #更新模板中的图
        self.mainwin.tm.add_elements(ele_list)
        
        #添加完成后更新界面
        self.mainwin.update()




