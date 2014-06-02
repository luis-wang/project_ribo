#coding:utf8
'''
本类包含的是，当匹配工作开始后从外面获取的样本图片，需要和模板相比较 
'''
import cv2
import uuid
import numpy as np
from math import sqrt,ceil,fabs

from globals import dpi
from tmpl import TM
from myutils import _getpxs
from element import Element

class Sample(object):

    def __init__(self, imgsrc, isvideo=False, th=150):
        '''
        Constructor,这应该是一个已经获取到的确定的图片了 imgsrc
        '
        '''
        if imgsrc != None:
            h,w,channel = imgsrc.shape
            self.w = w
            self.h = h
            
            self.pw = 0; self.ph = 0 #找出最大的纸张的长与宽
            
            self.ele_list = []     #保存检测到的样本下面的所有ele元素
            self.imgsrc = imgsrc

            self.bg = np.zeros(imgsrc.shape, np.uint8)
            
            self.paper_found = False #是否找到了纸张
            
            
            #############################################
            self.isvideo = isvideo #isvideo表示些样本是怎么来的，如果来自视频，那其中扫描的纸张肯定小于整个imgsrc
                        
            #样本识别需要的一些参数
            self.paper_threshold = th      #
            self.area_threashold = 200*200
            
            self.find_paper()
            
    
                
            #计算出所有的字体条形码的轮廓
            self.calcu_blob_outline()
            
            #标识出所有的元素轮廓,然后生成一系列的元素列表
            self.mark_object()
    
    def get_sap_img(self):
        "获取样本的图像格式"
        return self.imgsrc
    
    
    def find_paper(self):
        "找出最大的纸张，以便下面的计算"
        gray = cv2.cvtColor(self.imgsrc.copy(), cv2.COLOR_BGR2GRAY)
        
        ret,thresh = cv2.threshold(gray, self.paper_threshold, 255, cv2.THRESH_BINARY)
        
        dilate = cv2.dilate(thresh,None)
        erode = cv2.erode(dilate,None)
        
        #cv2.imshow('erode', erode)
        
        
        # Find contours with cv2.RETR_CCOMP
        contours,hierarchy = cv2.findContours(erode, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        
        #print 'len :',len(contours)
        max_area = 0
        best_cnt = None
        
        #这里就找出了最大的一个矩形，也就是纸张
        for i,cnt in enumerate(contours):
            # Check if it is an external contour and its area is more than 100
            if hierarchy[0,i,3] == -1:
                    area = cv2.contourArea(cnt)         #面积
                    perimeter = cv2.arcLength(cnt,True) #周长
                    
                    if area >= self.area_threashold:
                        if area > max_area:
                            max_area = area
                            best_cnt = cnt
        
        #找到了最大的纸张
        if best_cnt != None:
            self.paper_found = True       
            x,y,w,h = cv2.boundingRect(best_cnt)
            self.pw = w
            self.ph = h
            
            #print '最大周长：',w,h  , '源的周长：',self.w , self.h  
            
            cv2.rectangle(self.imgsrc, (x,y), (x+w,y+h), (100,255,0),2) 
            #cv2.imshow('draw paper', self.imgsrc)
            
            #剪切出纸张
            #cv2.imshow('paper', self.imgsrc[y:y+h,x:x+w])
            #self.imgsrc = self.imgsrc[y:y+h,x:x+w]
            
            '''
            cv2.imshow('most paper', self.imgsrc)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            '''
        
        #未找到最大纸张，需要改变参数         
        else:
            print '未找到最大纸张，需要改变参数         '
        

    def calcu_blob_outline(self):
        "对原图进行变形，把相关的blob放大，然后给下一步长轮廓做优化"
        #copy原图 ，有可能不是规整的纸张，需要从中找出一个最大的矩形
        img = self.imgsrc.copy()
        
        #转换成灰度图
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        #高斯模糊效果不错 ,需要反转一下
        adap_gauss = cv2.adaptiveThreshold(img, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,21)
        
        
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
        
        #保存到实例的变量中
        self.opening = opening
    
    
    def mark_object(self):
        '''
        '找到近似的矩形,并返回出来
        '''
        img = self.imgsrc.copy()
        imgobj = self.opening.copy()
        
        #height, width, channel = img.shape
        height = img.shape[0]

        contours,hierarchy = cv2.findContours(imgobj, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        
        for i,cnt in enumerate(contours):
            # Check if it is an external contour and its area is more than 100
            if hierarchy[0,i,3] == -1 and cv2.contourArea(cnt)>100:

                #依次是左顶点的位置，宽和长
                x,y,w,h = cv2.boundingRect(cnt)
                
                #过滤出高度太高的矩形,至少应该小于总高的一半
                if h < int(height/2.0):
                    #1.根据每个轮廓生成对应的元素
                    ele = Element('', w,h, x,y)
                    self.ele_list.append(ele)
                    

                    #m = cv2.moments(cnt)
                    #找出形状的中心
                    #cx,cy = m['m10']/m['m00'],m['m01']/m['m00']
                    #画出矩形的中心点
                    #cv2.circle(img,(int(cx),int(cy)),3,255,-1)


    
    def get_res(self, tm):
        "传递来的是模板tm, 返回此样本检测的最终结果 "
        #1.将样本复制一份
        bg = self.imgsrc.copy()
        
        
        #2.找出所有的矩形
        for e in self.ele_list:
            x,y,w,h = e.x,e.y,e.w,e.h
            
            #1.标出矩形的框
            cv2.rectangle(bg, (x,y), (x+w,y+h), (0,0,255),2) 
            
            #2.画出每个条形码的中心
            centroid_x = x + int(w/2)
            centroid_y = y + int(h/2)
            cv2.circle(bg, (centroid_x,centroid_y), 6, (0,255,0),-1) #绿色点
            
            #3.在模板中查找是不是有有相应的矩形
            '''
            #循环模板每一个元素，并计算与当前的矩形的距离
            find_tmpl = False  
            for e0 in tm.ele_list:
                x0,y0,w0,h0 = e0.x,e0.y,e0.w,e0.h
                
                dist = sqrt((x0-x)*(x0-x) + (y0-y)*(y0-y))
                #这里在模板中至少有一个和当前的距离为0或相差不大的值，如果没有那就要标红
                if dist ==0:
                    find_tmpl = True
                    break
            
            #4.如果没有找到,并且已经有模板的情况下，才需要标红
            if find_tmpl == False:
                cv2.circle(bg, (centroid_x,centroid_y), 10, (255,0,0),-1)            
            '''

        return bg
        
if __name__ == '__main__':
    '''
    imgsrc = np.zeros((100,400), np.uint8)
    imgsrc = cv2.bitwise_not(imgsrc)
    '''
    imgsrc = cv2.imread('img/s1.png')
    
    img = Sample(imgsrc).get_res(None)
    
    
    cv2.imshow('img',img)
    cv2.waitKey(0)   

        
        