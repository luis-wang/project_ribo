#coding:utf8
'''
此类处理所有逻辑的主窗口,与ui生成的类完全没有关系 
'''
import sys
from PyQt4.QtGui import QMainWindow, QDialog,QApplication
from main_window import new_main_window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    ui = new_main_window()
    ui.show()
    sys.exit(app.exec_())

