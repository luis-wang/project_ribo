#coding:utf8
'''

'''
from math import *
import cv2
import numpy as np

dpi = 72

ele_w,ele_h = 200,60
left_margin,top_margin = 10,10
row_num,col_num,h_space,v_space = 2,2, 20,20

def _getpxs(f):
    #从浮点数转换成像素的大小
    return int(ceil(f/25.4*dpi))
    

#先算一行 为了得到一系列的矩形坐标(x,y,w,h) 只有x,y会变化
#ele_w = _getpxs(ele_w)
#ele_h = _getpxs(ele_h)

gen_rects = []

#一行一行地产生矩形，有多少列就有多少个行元素
for c in range(col_num):
    for r in range(row_num):
        #内层循环中这一列列的元素，所以x值是相同的
        x = left_margin + c * (ele_w + h_space)
        y = top_margin +  r * (ele_h + v_space)
        gen_rects.append([x,y, ele_w,ele_h])
        
print 'gen_rects = '
print gen_rects


img = np.zeros((600,800,3),np.uint8)
img = cv2.bitwise_not(img)

for rec in gen_rects:
    x,y,w,h = rec
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    
cv2.imshow('winname', img)
cv2.waitKey()    
    
    






