#coding:utf8
'''
设置全局变量
颜色：
淡绿：132,244,132
淡蓝：86,170,255

用到的颜色网站 ：
选择一个颜色  http://rgb.phpddt.com/

'''

dpi = 100   #一般设置成100，也可以是72
freq = 30   #画面更新的频率 ms

lm = .28  #.4in 表示离左边的距离，值应该是0-1
bm = .16  #.3in 表示到下边的距离 

#默认的每次移动的距离
move_dis = 5.0 #毫米

#从哪里启动界面
init_from = 'path'  #如果设置为path，那直接就从给定的图像打开 

#初始化图片的名称
init_img_name = r'D:\data\aptana34workspace\pyqtexample\example1\carve_project\img\img_1931_s.jpg'


#一些测试的图片
ims = ['img/riboimg/s1.png',
       'img/riboimg/y1.png',
       'img/riboimg/y2.png',
       'img/riboimg/y3.png',]



