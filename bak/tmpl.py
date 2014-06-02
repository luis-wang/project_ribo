#coding:utf8

import cv2
import numpy as np
from opencv_proc import label_color
import uuid
from operator import itemgetter,attrgetter
from math import sqrt,ceil,fabs

from globals import dpi

'''
保存操作过程中的模板
'''

def _getpxs(f):
    #从浮点数转换成像素的大小
    return int(ceil(f/25.4*dpi))

class TM(object):
    
    def __init__(self,imgpath=None,w=0,h=0):
        
        self.t = ''             #t表示的是此模板是怎么创建起来的 'path'  'wh'
        self.ele_list = []      #保存模板下面的所有ele元素
        
        
        #如果给了模板图片的路径 
        if imgpath:
            self.t = 'path' #通过指定路径来设置的
            self.imgpath = imgpath
            self.imgsrc  = cv2.imread(imgpath)
        elif w!=0 and h!=0:
            self.t = 'wh' #通过宽和高来设置的
            self.imgsrc = np.zeros((h,w,3), np.uint8)
            self.imgsrc = cv2.bitwise_not(self.imgsrc)
            
            self.bg = np.zeros((h,w,3), np.uint8)
            self.bg = cv2.bitwise_not(self.bg)            
             
        #第一种，通过截图一个模板图像
        if self.t == 'path':
            self.imgpath = imgpath
    
            self.imgsrc  = cv2.imread(imgpath)
            #保存一个白板，每次都用作背景
            self.bg = np.zeros(self.imgsrc.shape, np.uint8)
            #self.bg = cv2.cvtColor(self.bg, cv2.COLOR_GRAY2BGR)
            self.bg = cv2.bitwise_not(self.bg)
            
            self.tmpl_bg = None #默认没有设置模板
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
            
            #标识出轮廓并保存到self变量
            self.mark_object()
            
            #初始化完毕后，都要重新画图像
            #self.re_draw_img()
        
        #通过长和高来设置的
        elif self.t == 'wh':
            pass

    def set_w_h(self,w,h):
        ##直接传递的是浮点型
        self.t = 'wh' #通过宽和高来设置的
        """
        "把w,h中大的一个设置为1000像素，小的那个取ceil值
        """
        
        #这里需要根据dpi转换成相应像素的图像大小       
        #w, h = int(ceil(w/25.4*dpi)), int(ceil(h/25.4*dpi))
        
        '''
        if w > h:
            self.w = 1000
            self.factor = 1000.0/w                  #得到放大的因子
            self.h = int(round(h * self.factor))     #按比例放大h
        else:
            self.h = 1000
            self.factor = 1000.0/h
            self.w = int(round(w * self.factor))
            
        print 'self.w, self.h =----- ',self.w, self.h
        
        
        self.per_mm = float(w)/self.w #计算每一像素是多少毫米
        self.per_px = float(self.w)/w #每一毫米表示多少像素
        
        print '单位像素表示的毫米数:',self.per_mm
        '''
        
        
        self.w,self.h = w,h
        
        #乱了
        self.imgsrc = np.zeros((self.w, self.h, 3), np.uint8)
        self.imgsrc = cv2.bitwise_not(self.imgsrc)
        
        self.bg = np.zeros((self.w, self.h, 3), np.uint8)
        self.bg = cv2.bitwise_not(self.bg)        
        
    def _calc(self,x):
        """计算转换成像素后的大小 """
        return int(round(self.factor * x))
        
        
    def add_elements(self, ele_list): 
        '直接添加新元素'
        
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
            cv2.rectangle(img, (x,y),(x+w,y+h),(0,0,255),1)                   
        
        self.imgsrc = img
        
    def get_tmpl(self):
        """
        "每次都从这里返回模板
        """
        return self.imgsrc.copy()
    
                            
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
                color = label_color()
                
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
                    
                #cv2.imshow('cnt',img)
                #cv2.waitKey(0)                  
        
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
        
    

        
    def find_out_rect_by_point(self, pnt):
        """
        "通过一个点判断是不是在相应的相应的矩形中
        "pnt = (x,y),rects = [(x,y,w,h),(x1,y1,w1,h1),]
        """
        for rect_dic in self.rect_list:
            rect = rect_dic['new'] #只取最新的
            
            #x应该在宽的长度以内 
            inwidth = pnt[0] >= rect[0] and pnt[0] <= rect[0]+rect[2]
            inheight= pnt[1] >= rect[1] and pnt[1] <= rect[1]+rect[3]
            
            if inwidth and inheight:
                #return rect
                return rect_dic['name'] #返回的是矩形的名称
                break
        return None 

    
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
    
    
    def set_new_rects(self, selected_rects, dict1):
        """
        "每次把new的相应值增加就行了
        """

        for rect_dict in self.rect_list:
            if rect_dict['name'] in selected_rects:
                print '设置开始.....:',rect_dict
                #这里为什么会出错
                #rect_dict['new'][0] = rect_dict['new'][0] + dict1['r'] - dict1['l'] #计算x轴的移动距离
                #rect_dict['new'][1] = rect_dict['new'][1] + dict1['d'] - dict1['u']
                
                a,b,c,d = rect_dict['new']
                a = a + dict1['r'] - dict1['l']
                b = b + dict1['d'] - dict1['u']
                rect_dict['new'] = [a,b,c,d]
          
                print '设置完成.....new:',rect_dict
               
        print ''
    
    
    def set_as_template(self):
        """
        "设置模板，其实就是保存的一系列的矩形的位置,还有一个画有蓝色矩形框的背景
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
    
    tm = TM(w=200,h=100)
    cv2.imshow('show', tm.imgsrc)
    cv2.waitKey()
    
    '''
    # [25, 52, 160, 44] x y w h
    x, y, w, h = 25, 52, 160, 44
    cvm = TM('img/img_1931_s.jpg')
    
    print '---',cvm.imgsrc.shape,type(cvm.imgsrc.shape)
    cv2.rectangle(cvm.imgsrc, (25,52), (25+160,52+44), (0,255,0),3)
    cv2.imshow('winname', cvm.imgsrc)

    ball = cvm.imgsrc[ y:y+h, x:x+w]  #tmp_img[x:x+h,y:y+w] = src_img[y:y+h, x:x+w]
    
    cv2.imshow('ball', ball)
    cv2.waitKey()
    '''
    
    print 'end..'
    
    
       
        
        
        