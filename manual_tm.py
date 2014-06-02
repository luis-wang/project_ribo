#coding:utf8

import cv2
import numpy as np
import uuid
from operator import itemgetter,attrgetter
from math import sqrt,ceil,fabs

from globals import dpi
from tmpl import TM
from myutils import _getpxs
from element import Element
from tmpl import TM


class Manual_tm(TM):
    '''
    #这是手工创建的模板，需要一个个手工添加，调整，然后才能当作模板使用
    '''

    def __init__(self, w, h):
        '''从长和宽设置一个模板'''
        
        TM.__init__(self)
        
        #长与宽
        self.w, self.h = w, h
        
        #设置背景
        bg = np.zeros((h,w,3), np.uint8)
        self.bg = cv2.bitwise_not(bg)
        
        
        
        
        
        
        
        
        
        
        
        
             
        