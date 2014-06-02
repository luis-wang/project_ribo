# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'set_paper.ui'
#
# Created: Fri May 02 20:04:26 2014
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(298, 274)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(90, 220, 120, 23))
        self.pushButton.setMinimumSize(QtCore.QSize(120, 0))
        self.pushButton.setMaximumSize(QtCore.QSize(120, 16777215))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 110, 261, 81))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget = QtGui.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 241, 22))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.custom_w_Edit = QtGui.QLineEdit(self.layoutWidget)
        self.custom_w_Edit.setEnabled(True)
        self.custom_w_Edit.setMinimumSize(QtCore.QSize(80, 0))
        self.custom_w_Edit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.custom_w_Edit.setObjectName(_fromUtf8("custom_w_Edit"))
        self.horizontalLayout_2.addWidget(self.custom_w_Edit)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.custom_h_Edit = QtGui.QLineEdit(self.layoutWidget)
        self.custom_h_Edit.setMinimumSize(QtCore.QSize(80, 0))
        self.custom_h_Edit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.custom_h_Edit.setObjectName(_fromUtf8("custom_h_Edit"))
        self.horizontalLayout_2.addWidget(self.custom_h_Edit)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 10, 261, 81))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.layoutWidget1 = QtGui.QWidget(self.groupBox_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 40, 241, 22))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtGui.QComboBox(self.layoutWidget1)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "纸张设置", None))
        self.pushButton.setText(_translate("Dialog", "确定", None))
        self.groupBox.setTitle(_translate("Dialog", "自定义大小", None))
        self.label_2.setText(_translate("Dialog", "宽：", None))
        self.label_3.setText(_translate("Dialog", "高：", None))
        self.groupBox_2.setTitle(_translate("Dialog", "标准大小", None))
        self.label.setText(_translate("Dialog", "纸张大小设置(宽x高):", None))
        self.comboBox.setItemText(0, _translate("Dialog", "请选择", None))
        self.comboBox.setItemText(1, _translate("Dialog", "600x600", None))
        self.comboBox.setItemText(2, _translate("Dialog", "800x600", None))
        self.comboBox.setItemText(3, _translate("Dialog", "1000x600", None))
        self.comboBox.setItemText(4, _translate("Dialog", "1000x800", None))
        self.comboBox.setItemText(5, _translate("Dialog", "1000x1000", None))

