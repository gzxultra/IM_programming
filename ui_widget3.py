# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled3.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_messageBox(object):
    def setupUi(self, messageBox):
        messageBox.setObjectName("messageBox")
        messageBox.resize(200, 100)
        self.label = QtWidgets.QLabel(messageBox)
        self.label.setGeometry(QtCore.QRect(50, 20, 141, 41))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.buttonBox = QtWidgets.QDialogButtonBox(messageBox)
        self.buttonBox.setGeometry(QtCore.QRect(20, 60, 164, 32))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(messageBox)
        self.buttonBox.clicked['QAbstractButton*'].connect(messageBox.hide)
        QtCore.QMetaObject.connectSlotsByName(messageBox)

    def retranslateUi(self, messageBox):
        _translate = QtCore.QCoreApplication.translate
        messageBox.setWindowTitle(_translate("messageBox", "Dialog"))
        self.label.setText(_translate("messageBox", "<html><head/><body><p><span style=\" font-size:14pt;\">密码错误，请重试</span></p></body></html>"))

