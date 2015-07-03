# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled2.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(640, 480)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(210, 30, 361, 291))
        self.textBrowser.setObjectName("textBrowser")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(210, 348, 281, 91))
        self.textEdit.setObjectName("textEdit")
        self.textBrowser_2 = QtWidgets.QTextBrowser(Form)
        self.textBrowser_2.setGeometry(QtCore.QRect(10, 60, 181, 381))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.sendButton = QtWidgets.QPushButton(Form)
        self.sendButton.setEnabled(False)
        self.sendButton.setGeometry(QtCore.QRect(500, 400, 68, 41))
        self.sendButton.setAutoFillBackground(True)
        self.sendButton.setStyleSheet("alternate-background-color: rgb(0, 255, 255);")
        self.sendButton.setObjectName("sendButton")
        self.clearButton = QtWidgets.QPushButton(Form)
        self.clearButton.setGeometry(QtCore.QRect(500, 349, 68, 41))
        self.clearButton.setObjectName("clearButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(60, 30, 71, 16))
        self.label.setObjectName("label")
        self.label.setBuddy(self.textBrowser_2)

        self.retranslateUi(Form)
        self.textEdit.textChanged.connect(Form.enableSendButton)
        self.sendButton.clicked.connect(Form.sendMessage)
        self.clearButton.clicked.connect(self.textBrowser.clear)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.textEdit, self.sendButton)
        Form.setTabOrder(self.sendButton, self.clearButton)
        Form.setTabOrder(self.clearButton, self.textBrowser)
        Form.setTabOrder(self.textBrowser, self.textBrowser_2)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.sendButton.setText(_translate("Form", "发送"))
        self.clearButton.setText(_translate("Form", "清屏"))
        self.label.setText(_translate("Form", "好友列表"))

