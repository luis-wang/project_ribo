#coding:utf8

import cv2
import uuid
import numpy as np
from math import sqrt,ceil,fabs

from globals import dpi
from tmpl import TM
from myutils import _getpxs
from element import Element

import win32api  
import win32con

class Auto_tm(TM):
    '''
    #这样的模板是自动从摄像头，或一个给定的图片路径生成的，把其中的元素分离出来，然后找出相应的矩形 
    '''
    def __init__(self,imgpath=None, img=None):
        '''imgpath为给定的模板路径 img为内存图片，可以直接使用的,两者只有其中之一不为空'''
        TM.__init__(self)
        self.imgpath = imgpath
        self.imgsrc = img
        
        #如果给了模板图片的路径 
        if imgpath != None:
            
            win32api.MessageBox(win32con.NULL, imgpath, 'imgpath!', win32con.MB_OK)  
            
            self.imgsrc = cv2.imread(imgpath)
            win32api.MessageBox(win32con.NULL, str(type(self.imgsrc)), 'type(self.imgsrc)', win32con.MB_OK) 
            
            #初始化背景，与给定图像一样大
            bg = np.zeros(self.imgsrc.shape, np.uint8)
            self.bg = cv2.bitwise_not(bg)
        #给的直接是内存图片
        elif img != None:
            bg = np.zeros(self.imgsrc.shape, np.uint8)
            self.bg = cv2.bitwise_not(bg)

        #长与宽
        self.h, self.w, channel = self.imgsrc.shape

        
        ############################################################
        
        
        
        self.tmpl_rects = None #保存模块的排列过序的矩形列表


        #保存从原图片中找到的所有blob，并且已经用红色框标识出来了，每次都在这上面计算
        self.red_blob = None
        
        self.contours = []
        self.rects = [] #轮廓相应的矩形
        
        
        #保存所有矩形和相应移动的距离[{"rect":(x,y,w,h),'l':0, 'r':10, 'u':0, 'd':0,},]
        self.moved_rects = []
        
        #这里把每次移动后的位置重新立即计算并保存起来，然后下一次的计算都基于此
        self.curr_rects = [] #[{'a':[x,y,w,h],'b':[x,y,w,h]},...]
        
        self.res = None #每次保存处理后显示的结果 
            
        #计算出所有的字体条形码的轮廓
        self.blob_outline_img = self.calcu_blob_outline()
        
        #标识出所有的元素轮廓,然后生成一系列的元素列表
        self.mark_object()
        
                 
    def calcu_blob_outline(self):
        #img = cv2.imread(imgsrc,0)
        #cv2.imshow('img', img)
        
        #判断是不是灰度图
        self.img_gray = cv2.cvtColor(self.imgsrc, cv2.COLOR_BGR2GRAY)
        
        #高斯模糊效果不错 ,需要反转一下
        adap_gauss = cv2.adaptiveThreshold(self.img_gray, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,21)
        
        #cv2.imshow('adap_gauss', adap_gauss)
        #cv2.waitKey(0)
        
        '''
        #Otsu's thresholding效果也不错
        ret2,Otsu = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        cv2.imshow('Otsu', Otsu)
        '''
    
        kernel = np.ones((7,7),np.uint8)
        opening = cv2.morphologyEx(adap_gauss, cv2.MORPH_CLOSE, kernel)
        
        #cv2.imshow('opening', opening)
    
    
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        return opening
    
    
    def mark_object(self):
        '''
        '找到近似的矩形,并返回出来
        '''
        img = self.imgsrc.copy()
        imgobj = self.blob_outline_img.copy()
        
        height, width, channel = img.shape
        back = self.bg.copy()
        
        filter_contours = [] #保存有用的轮廓
        filter_rects = []    #保存轮廓相应的矩形
        
        #保存的是各轮廓的新旧值和name值
        self.rect_list = []
        
        # Find contours with cv2.RETR_CCOMP
        contours,hierarchy = cv2.findContours(imgobj,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
        
        for i,cnt in enumerate(contours):
            # Check if it is an external contour and its area is more than 100
            if hierarchy[0,i,3] == -1 and cv2.contourArea(cnt)>100:
                #color = label_color()
                
                #依次是左顶点的位置，宽和长
                x,y,w,h = cv2.boundingRect(cnt)
                
                #过滤出高度太高的矩形,至少应该小于总高的一半
                if h < int(height/2.0):
                    #画出矩形,并且画到self.bg上面，然后以后就在self.bg上面移动打印等操作
                    cv2.rectangle(back,(x,y),(x+w,y+h),(0,0,255),2)
                    #filter_contours.append(cnt)
                    #filter_rects.append([x,y,w,h])
                    rect1 = [x,y,w,h]
                    #初始化一个list
                    self.rect_list.append({'name':str(uuid.uuid4().get_hex().upper()),'old':rect1,'new':rect1})
                    
                    #根据每个轮廓生成对应的元素
                    ele = Element('', w,h, x,y)
                    self.ele_list.append(ele)
                    
                    
                    
                #m = cv2.moments(cnt)
                #找出形状的中心
                #cx,cy = m['m10']/m['m00'],m['m01']/m['m00']
                #画出矩形的中心点
                #cv2.circle(img,(int(cx),int(cy)),3,255,-1)
        
        #cv2.imshow('mark_object', back)
        #cv2.waitKey(0)
        
        self.res = self.bg 
        self.contours = filter_contours
        self.rects = filter_rects
         
        #return (img,filter_contours,filter_rects)
        
    

    
    def draw_rects(self, selected_rects):
        """
        "把一系列的矩形画出来 
        """
        #这里要是不新建一个对象，那每次都会在传入的img上直接绘制，所以结果可能会错
        src_img = self.imgsrc.copy()  
        if self.tmpl_bg != None:
            tmp_img = self.tmpl_bg.copy()
        else:
            tmp_img = self.bg.copy()
               
        #循环本身的所有矩形
        for rect_dict in self.rect_list:
            #-1-先把原图中的轮廓blob都移过来
            x,y,w,h = rect_dict['old']
            x1,y1,w1,h1 = rect_dict['new']
            
            tmp_img[y1:y1+h1, x1:x1+w1] = src_img[y:y+h, x:x+w]
            
            #-1.5-画出每个条形码的中心
            centroid_x = x1 + int(w1/2)
            centroid_y = y1 + int(h1/2)
            cv2.circle(tmp_img, (centroid_x,centroid_y), 6, (0,255,0),-1)
            
            #-2-每次都重新画出红绿的矩形
            if rect_dict['name'] in selected_rects:
                #选中的画绿框
                cv2.rectangle(tmp_img, (x1,y1), (x1+w1,y1+h1), (0,255,0),3)
            else:
                #未选中的画成别的color
                cv2.rectangle(tmp_img, (x1,y1), (x1+w1,y1+h1), (0, 0, 190),2)
            
            #-3-计算出当前样本是否与模板相差太多，相差了的就在里面画一个红色的框
               
            if self.tmpl_rects != None:
                #循环每一个模板，并计算与当前的矩形的距离
                find_tmpl = False  
                for tmpl_rect in self.tmpl_rects:
                    x0,y0,w0,h0 = tmpl_rect['new']
                    dist = sqrt((x0-x1)*(x0-x1) + (y0-y1)*(y0-y1))
                    #这里在模板中至少有一个和当前的距离为0或相差不大的值，如果没有那就要标红
                    if dist ==0:
                        find_tmpl = True
                        break
            
                #如果没有找到,并且已经有模板的情况下，才需要标红
                if find_tmpl == False:
                    cv2.circle(tmp_img, (centroid_x,centroid_y), 10, (255,0,0),-1)
            
        return tmp_img           
    
    
    
