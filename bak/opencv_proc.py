#coding:utf8
'''
Created on 2014-2-19

@author: Administrator
'''
import cv2
import math
import cv2.cv as cv
import numpy as np
import random
from PyQt4.QtGui import QImage

font = cv2.FONT_HERSHEY_SIMPLEX


class IplQImage(QImage):
    """
    http://matthewshotton.wordpress.com/2011/03/31/python-opencv-iplimage-to-pyqt-qimage/
    A class for converting iplimages to qimages
    """

    def __init__(self,iplimage):
        # Rough-n-ready but it works dammit
        alpha = cv.CreateMat(iplimage.height,iplimage.width, cv.CV_8UC1)
        cv.Rectangle(alpha, (0, 0), (iplimage.width,iplimage.height), cv.ScalarAll(255) ,-1)
        rgba = cv.CreateMat(iplimage.height, iplimage.width, cv.CV_8UC4)
        cv.Set(rgba, (1, 2, 3, 4))
        cv.MixChannels([iplimage, alpha],[rgba], [
        (0, 0), # rgba[0] -> bgr[2]
        (1, 1), # rgba[1] -> bgr[1]
        (2, 2), # rgba[2] -> bgr[0]
        (3, 3)  # rgba[3] -> alpha[0]
        ])
        self.__imagedata = rgba.tostring()
        super(IplQImage,self).__init__(self.__imagedata, iplimage.width, iplimage.height, QImage.Format_RGB32)

 

def cacu_distance(pt1,pt2):
    dist = math.hypot(pt2[0]-pt1[0], pt2[1]-pt1[1])
    #dist = math.hypot(x2-x1, y2-y1)
    return dist

def random_color():
    return (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))

def label_color():
    random_color = [(255,255,255),
                    (247,217,96),
                    (249,232,164),
                    (255,170,170),
                    (255,0,0),(255,255,0),
                    (170,255,86),
                    (86,255,255),
                    (0,127,255),(0,0,191),
                    (255,86,255)]
    
    return random.choice(random_color)

def label_lines(img, pt1, pt2, label, color):
    """对线段进行标注"""
    #先找到两个点的中点
    x = int((pt1[0]+pt2[0])/2.0)
    y = int((pt1[1]+pt2[1])/2.0)
    
    #写字
    # Python: cv2.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]) → None
    #cv2.putText(img,str(cacu_distance((x1,y), (x1, 0)))+'px',(x1-25,int(y/2.0)), font, 0.5,(205,0,255),1,cv2.CV_AA) #cv2.LINE_AA
    lable_x = x-25  #这两值都是字体的左下角的点
    lable_y = y+5
    
    if lable_x < 0:
        lable_x = x
    
    cv2.putText(img,str(label),(lable_x,lable_y), font, 0.5, color, 1, cv2.CV_AA)
    
    return img  





def gen_random_distance(min,dis):
    """找到一个范围的随机值"""
    return random.randint(min,dis)
    
    
def step2(imgobj):
    '''
    '找到近似的矩形
    '''
    img = cv2.imread(imgsrc)
    # Find contours with cv2.RETR_CCOMP
    contours,hierarchy = cv2.findContours(imgobj,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    
    for i,cnt in enumerate(contours):
        # Check if it is an external contour and its area is more than 100
        if hierarchy[0,i,3] == -1 and cv2.contourArea(cnt)>100:
            color = label_color()
            
            #依次是左顶点的位置，宽和长
            x,y,w,h = cv2.boundingRect(cnt)
            #画出矩形
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    
            m = cv2.moments(cnt)
            #找出形状的中心
            cx,cy = m['m10']/m['m00'],m['m01']/m['m00']
            #画出矩形的中心点
            cv2.circle(img,(int(cx),int(cy)),3,255,-1)
            
            
            #-1-画出与上边缘的距离并标注
            x1 = gen_random_distance(x,x+w)
            cv2.line(img, (x1,y), (x1, 0),color,1)          
            img = label_lines(img,(x1,y), (x1, 0), str(cacu_distance((x1,y), (x1, 0)))+'px', color)
            
            #-2-画出与左边缘的距离 并标注
            y1 = gen_random_distance(y,y+h)
            cv2.line(img, (0,y1), (x, y1),color,1)
            
            img = label_lines(img,(0,y1), (x, y1), str(cacu_distance((0,y1), (x, y1)))+'px',color)            
                    
            
    
    #cv2.imshow('img',img)
    #cv2.waitKey(0)
    return img




def get_result_img():
    """
    "直接把处理结果返回给pyqt
    """
    res1  = step1(imgsrc)
    imgres = step2(res1)
    
    #imgres = cv2.imread('img/3.png')
    return imgres

def load_src_img():
    """第一次把原图像打开"""
    imgres = cv2.imread(imgsrc)
    return imgres    


def clicked_img(img):
    '''用于测试'''
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    #res = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    x = y = 100
    w = 100
    h = 100
    
    #画一个矩形
    cv2.rectangle(img, (x,y), (x+w,y+h),(255,255,0),2)  
    print 'draw end'
    return img


def mark_object(imgobj):
    '''
    '找到近似的矩形,并返回出来
    '''
    img = cv2.imread(imgsrc)
    
    height, width = imgobj.shape
    
    filter_contours = [] #保存有用的轮廓
    filter_rects = []    #保存轮廓相应的矩形
    
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
                #画出矩形
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),1)
                filter_contours.append(cnt)
                filter_rects.append([x,y,w,h])
                
            #cv2.imshow('cnt',img)
            #cv2.waitKey(0)                  
    
            #m = cv2.moments(cnt)
            #找出形状的中心
            #cx,cy = m['m10']/m['m00'],m['m01']/m['m00']
            #画出矩形的中心点
            #cv2.circle(img,(int(cx),int(cy)),3,255,-1)
    
    #cv2.imshow('img',img)
    #cv2.waitKey(0)    
    return (img,filter_contours,filter_rects)


def find_out_rect_by_point(pnt, rects):
    """
    "通过一个点判断是不是在相应的相应的矩形中
    "pnt = (x,y),rects = [(x,y,w,h),(x1,y1,w1,h1),]
    """
    for rect in rects:
        #x应该在宽的长度以内 
        inwidth = pnt[0] >= rect[0] and pnt[0] <= rect[0]+rect[2]
        inheight= pnt[1] >= rect[1] and pnt[1] <= rect[1]+rect[3]
        
        if inwidth and inheight:
            return rect
            break
    return None

def draw_rects(img, selected_rects):
    """
    "把一系列的矩形画出来 
    """
    #这里要是不新建一个对象，那每次都会在传入的img上直接绘制，所以结果可能会错
    tmp_img = img.copy()
         
    for rect in selected_rects:
        x,y,w,h = rect
        cv2.rectangle(tmp_img,(x,y),(x+w,y+h),(0,255,0),3)
    
    return tmp_img


def draw_moved_rects(imgsrc, bg, curr_rects):
    """
    "画出移动后的图像,移动后的图像是自定义的白色背景加上各个轮廓里面的图案
    "moved_rects : [{"rect":(x,y,w,h),'r':10,'b':0},]
    """
    tmp_img = bg.copy()
    
    for rect in curr_rects:
        #这里把原图中的条形码全部移过来
        
        x1,y1,w1,h1 = rect['a']
        x,y,w,h = rect['b']
        
        if x1 == x and y1 == y:
            cv2.rectangle(tmp_img,(x,y),(x+w,y+h),(255,255,0),3)
        else:
            roi = imgsrc[x1:x1+h1,y1:y1+w1] #前面加的是高，后面加的是宽
            print 'x1,y1,w1,h1 = ',x1,y1,w1,h1
            
            
            #这里是画的边框，用于标记
            
            print 'x,y,w,h = ',x,y,w,h
            tmp_img[x:x+h, y:y+w] = roi
            cv2.rectangle(tmp_img,(x,y),(x+w,y+h),(0,255,0),2)            
        
    
    
    return tmp_img


def step1(img):
    #img = cv2.imread(imgsrc,0)
    cv2.imshow('img', img)
    
    #判断是不是灰度图
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #高斯模糊效果不错 ,需要反转一下
    adap_gauss = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,7,7)  #21,21
    
    cv2.imshow('adap_gauss', adap_gauss)
    #cv2.waitKey(0)
    
    '''
    #Otsu's thresholding效果也不错
    ret2,Otsu = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow('Otsu', Otsu)
    '''

    kernel = np.ones((7,7),np.uint8)
    opening = cv2.morphologyEx(adap_gauss, cv2.MORPH_CLOSE, kernel)
    
    cv2.imshow('opening', opening)


    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #return opening

imgsrc = 'img/2.png' #diao1.png  img_1931_s.jpg

if __name__ == '__main__':
    
    img = cv2.imread(imgsrc)
    res1  = step1(img)
    #mark_object(res1)
    #res2 = step2(res1)
    pass



