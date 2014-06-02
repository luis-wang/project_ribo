#coding:utf8

import cv2
import numpy as np
from globals import dpi,move_dis


class TM(object):
    
    def __init__(self):
        self.w = 0; self.h = 0  #分别保存的是模板的长与宽,实际表示的是像素的多少
        self.ele_list = []      #保存模板下面的所有ele元素
        self.bg = None          #背景
        self.imgsrc = None      #每次返回给界面显示的合并图像
        
        self.dis = move_dis     #始始化时每次移动的距离
        self.err_dis = 1.0      #误差值 
        #保存的是选中的元素
        self.selected_elements = []
        
        #只要是在初始化模板，那就设置为默认的模板
        self.as_tmpl = True
                
    
    def add_elements(self, ele_list): 
        '在之前已经产生的模板中添加新元素'
        
        if self.bg == None:
            print '模板的背景还没有生成！！'
            return
        
        #在已存在的元素中添加新元素
        for i in ele_list:
            self.ele_list.append(i)
        
        print 'self.ele_list = ',self.ele_list 
        
        #背景重置
        img = self.bg.copy()
        #重新画出所有的元素
        for e in self.ele_list:
            x,y,w,h = int(e.x), int(e.y), int(e.w), int(e.h)
            print 'x,y,w,h = ',x,y,w,h
            cv2.rectangle(img, (x,y),(x+w,y+h),(0,0,255),2)                   
        
        self.imgsrc = img
        
        
    def rm_element(self):
        """去掉选中的元素"""
        tmp_eles = self.selected_elements[:] #copy.deepcopy(self.selected_elements)
        
        #1.只要在选中的元素列表中，就从所有的元素中去掉
        for e in tmp_eles:
            if e in self.ele_list:
                self.ele_list.remove(e)
        
        #2.再把选中的列表置空
        self.selected_elements = []
                     
        
    def get_tmpl(self):
        """每次都从这里返回生成后的模板"""
        bg = self.bg.copy()
        
        #1.在空白的背景上面画出一系列的元素
        for e in self.ele_list:
            #先只画出没有选中的
            if not e in self.selected_elements:
                x,y,w,h = e.x, e.y, e.w, e.h
                cv2.rectangle(bg, (x,y), (x+w,y+h), (86,170,255), -1)
        
        #2.标识出选中的那些元素
        for e in self.selected_elements:
            x,y,w,h = e.x, e.y, e.w, e.h
            cv2.rectangle(bg, (x,y), (x+w,y+h), (247,79,180), -1)
            
        #3.对选中的元素，标识出它的尺寸与各个方位的距离 

        return bg
    
    
    def move_elements(self, dire, flag, dis=0):
        '''移动选中的元素，传入方向和距离, flag表示的是正方向1，还是反方向-1'''
        
        #这里传来的dis可能是正负值
        if dis != 0:
            moved_dis = dis
        else:
            moved_dis = self.dis
        
        #只计算向右移动，向左的话就是负数
        if dire == 'r':
            for e in self.selected_elements:
                e.x = e.x + int(moved_dis)*flag #直接加就是了，反方向就是*一个负1
                
        elif dire == 'd':
            
            for e in self.selected_elements:
                e.y = e.y + int(moved_dis)*flag
                
                
    def change_element_dir(self):
        "将选中的所有矩形都旋转方向,位置不变，只是对调的长和宽"
        for e in self.selected_elements:
            x,y,w,h = e.x, e.y, e.w, e.h
            e.h = w
            e.w = h       
                

    def find_out_rect_by_point(self, pnt):
        """
        "通过一个点判断是不是在相应的相应元素中，如果是就直接返回相应元素
        "pnt = (x,y),rects = [(x,y,w,h),(x1,y1,w1,h1),]
        """
        for e in self.ele_list:
            x,y,w,h = e.x, e.y, e.w, e.h
            
            #x应该在宽的长度以内, y应该在高度以内 
            inwidth = pnt[0] >= x and pnt[0] <= x+w
            inheight= pnt[1] >= y and pnt[1] <= y+h     
            
            #确实满足在某个选中的元素内
            if inwidth and inheight:
                if e in self.selected_elements:
                    self.selected_elements.remove(e)
                else:
                    self.selected_elements.append(e)
                break             
        
        
    def set_as_template(self):
        """
        "设置模板,还有一个画有蓝色矩形框的背景
        """
        #先清除之前的背景
        self.bg = np.zeros(self.imgsrc.shape, np.uint8)
        self.bg = cv2.bitwise_not(self.bg)        
        
        print '未排序列表：'
        for rect_dict in self.rect_list:
            print '--:',rect_dict
            x,y,w,h = rect_dict['new']
            cv2.rectangle(self.bg, (x,y), (x+w,y+h), (0,0,255),2)        

        #设置新的背景
        self.tmpl_bg = self.bg.copy()
        #把矩形把新的保存到模板中
        self.tmpl_rects = self.rect_list
        
        


if __name__ == '__main__':
    print 'start..'
    
    img = cv2.imread('img/img_1931_s.jpg')
    h,w,c = img.shape  #w,h,c =   1354 301 3
    print 'w,h,c = ',w,h,c
    bg = np.zeros(img.shape, np.uint8)
    bg = cv2.bitwise_not(bg)
    cv2.imshow('window',bg)
    cv2.waitKey()
    
    
    
    print 'end..'
    
    
       
        
        
        