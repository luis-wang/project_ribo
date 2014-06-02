# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting_dialog.ui'
#
# Created: Wed May 28 07:03:37 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Setting_Dialog(object):
    def setupUi(self, Setting_Dialog):
        Setting_Dialog.setObjectName(_fromUtf8("Setting_Dialog"))
        Setting_Dialog.resize(362, 431)
        self.groupBox = QtGui.QGroupBox(Setting_Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 30, 321, 101))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget = QtGui.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 291, 22))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.layoutWidget_2 = QtGui.QWidget(self.groupBox)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 60, 291, 22))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.layoutWidget_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit_err_dis = QtGui.QLineEdit(self.layoutWidget_2)
        self.lineEdit_err_dis.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_err_dis.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_err_dis.setObjectName(_fromUtf8("lineEdit_err_dis"))
        self.horizontalLayout_3.addWidget(self.lineEdit_err_dis)
        self.layoutWidget1 = QtGui.QWidget(Setting_Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(90, 360, 181, 25))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.okButton = QtGui.QPushButton(self.layoutWidget1)
        self.okButton.setMinimumSize(QtCore.QSize(80, 0))
        self.okButton.setMaximumSize(QtCore.QSize(80, 16777215))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout_2.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(self.layoutWidget1)
        self.cancelButton.setMinimumSize(QtCore.QSize(80, 0))
        self.cancelButton.setMaximumSize(QtCore.QSize(80, 16777215))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout_2.addWidget(self.cancelButton)
        self.groupBox_2 = QtGui.QGroupBox(Setting_Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 150, 321, 101))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.widget = QtGui.QWidget(self.groupBox_2)
        self.widget.setGeometry(QtCore.QRect(10, 20, 291, 21))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.paperSlider = QtGui.QSlider(self.widget)
        self.paperSlider.setMinimumSize(QtCore.QSize(163, 0))
        self.paperSlider.setMaximumSize(QtCore.QSize(163, 16777215))
        self.paperSlider.setMaximum(255)
        self.paperSlider.setSingleStep(0)
        self.paperSlider.setPageStep(5)
        self.paperSlider.setProperty("value", 100)
        self.paperSlider.setOrientation(QtCore.Qt.Horizontal)
        self.paperSlider.setObjectName(_fromUtf8("paperSlider"))
        self.horizontalLayout_4.addWidget(self.paperSlider)

        self.retranslateUi(Setting_Dialog)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Setting_Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Setting_Dialog)

    def retranslateUi(self, Setting_Dialog):
        Setting_Dialog.setWindowTitle(_translate("Setting_Dialog", "全局设置", None))
        self.groupBox.setTitle(_translate("Setting_Dialog", "操作", None))
        self.label.setText(_translate("Setting_Dialog", "每次移动长度(毫米)：", None))
        self.lineEdit.setToolTip(_translate("Setting_Dialog", "可精确到0.1毫米", None))
        self.label_2.setText(_translate("Setting_Dialog", "设置误差(毫米)：", None))
        self.lineEdit_err_dis.setToolTip(_translate("Setting_Dialog", "可精确到0.1毫米", None))
        self.okButton.setText(_translate("Setting_Dialog", "确定", None))
        self.cancelButton.setText(_translate("Setting_Dialog", "取消", None))
        self.groupBox_2.setTitle(_translate("Setting_Dialog", "操作", None))
        self.label_3.setText(_translate("Setting_Dialog", "图像灰度阀值(0-255):", None))
        self.paperSlider.setToolTip(_translate("Setting_Dialog", "<html><head/><body><p>调节此数值，以使视频或图像中的纸张更清晰</p></body></html>", None))

