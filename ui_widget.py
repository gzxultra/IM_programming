# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoginDlg(object):
    def setupUi(self, LoginDlg):
        LoginDlg.setObjectName("LoginDlg")
        LoginDlg.resize(425, 240)
        self.label = QtWidgets.QLabel(LoginDlg)
        self.label.setGeometry(QtCore.QRect(120, 10, 151, 141))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/invisible2.jpg"))
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(LoginDlg)
        self.widget.setGeometry(QtCore.QRect(80, 160, 243, 68))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.label1 = QtWidgets.QLabel(self.widget)
        self.label1.setObjectName("label1")
        self.gridLayout.addWidget(self.label1, 0, 0, 1, 1)
        self.loginButton = QtWidgets.QPushButton(self.widget)
        self.loginButton.setEnabled(False)
        self.loginButton.setDefault(True)
        self.loginButton.setObjectName("loginButton")
        self.gridLayout.addWidget(self.loginButton, 0, 2, 1, 1)
        self.label2 = QtWidgets.QLabel(self.widget)
        self.label2.setObjectName("label2")
        self.gridLayout.addWidget(self.label2, 1, 0, 1, 1)
        self.passwordEdit = QtWidgets.QLineEdit(self.widget)
        self.passwordEdit.setObjectName("passwordEdit")
        self.gridLayout.addWidget(self.passwordEdit, 1, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 2, 1, 1)
        self.userNameEdit = QtWidgets.QLineEdit(self.widget)
        self.userNameEdit.setObjectName("userNameEdit")
        self.gridLayout.addWidget(self.userNameEdit, 0, 1, 1, 1)
        self.label1.raise_()
        self.label2.raise_()
        self.userNameEdit.raise_()
        self.passwordEdit.raise_()
        self.loginButton.raise_()
        self.pushButton_2.raise_()
        self.userNameEdit.raise_()
        self.label.raise_()
        self.label1.setBuddy(self.userNameEdit)
        self.label2.setBuddy(self.passwordEdit)

        self.retranslateUi(LoginDlg)
        self.passwordEdit.textChanged['QString'].connect(LoginDlg.enableLoginButton)
        self.loginButton.clicked.connect(LoginDlg.login)
        self.pushButton_2.clicked.connect(self.userNameEdit.clear)
        self.pushButton_2.clicked.connect(self.passwordEdit.clear)
        QtCore.QMetaObject.connectSlotsByName(LoginDlg)
        LoginDlg.setTabOrder(self.userNameEdit, self.passwordEdit)
        LoginDlg.setTabOrder(self.passwordEdit, self.loginButton)
        LoginDlg.setTabOrder(self.loginButton, self.pushButton_2)

    def retranslateUi(self, LoginDlg):
        _translate = QtCore.QCoreApplication.translate
        LoginDlg.setWindowTitle(_translate("LoginDlg", "IM"))
        self.label1.setText(_translate("LoginDlg", "账号："))
        self.loginButton.setText(_translate("LoginDlg", "登陆"))
        self.label2.setText(_translate("LoginDlg", "密码："))
        self.pushButton_2.setText(_translate("LoginDlg", "清除"))

import logo_rc
