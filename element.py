#coding:utf8

'''
Created on 2014-5-6

@author: Administrator
'''

class Element(object):
    '''
    #保存的是画布中的所有元素，如条形码，二维码
    '''


    def __init__(self,tp, w,h, x=0,y=0):
        '''
        Constructor
        '''
        self.tp = tp #类型：条型码为barcode 二维码:dimcode
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        
        #这两个位置关系也要要
        #self.left_margin
        #self.top_margin
        
        
        
        
        
        
        