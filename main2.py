# -*- coding: utf-8 -*-

import sys

from class_ClientMessage import ClientMessage
from ui_widget import Ui_LoginDlg
from ui_widget2 import Ui_Form
from ui_widget3 import Ui_messageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import time


class IM_loginDlgImpl(QtWidgets.QDialog, Ui_LoginDlg):
    """QtGui.QWidget和界面设计时选择的类型一致"""
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self) # Ui_Form.setupUi
        #self.pushButton.clicked.connect(self.myPrint)   #槽函数不用加括号
    #def myPrint(self):                                #定义槽
        #self.hide()
    def enableLoginButton(self, text):
        self.loginButton.setEnabled(True)

    def login(self):
        userName = self.userNameEdit.text()
        password = self.passwordEdit.text()

        
        client.setLocalANDPort('127.0.0.1', 8808)
        client.setUsrANDPwd(userName, password)
        client.setToUsr('12073127')
        authentication = client.receiveMessage()
        if authentication == True:
            self.hide()
            ex2.show()
            client.receiveMessage()
        else:
            ex3.show()

class IM_FormImpl(QtWidgets.QDialog, Ui_Form):
    """QtGui.QWidget和界面设计时选择的类型一致"""
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self) # Ui_Form.setupUi
        #self.pushButton.clicked.connect(self.myPrint)   #槽函数不用加括号
    #def myPrint(self):                                #定义槽
        #self.hide()
    def enableSendButton(self):
        # print len(self.textEdit.toPlainText()) 
        self.sendButton.setEnabled(len(self.textEdit.toPlainText()) > 0)

    def sendMessage(self):
        message = self.textEdit.toPlainText()
        # print "I said %s" %message
        #格式化当前的时间
        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        client.udpCliSock.sendto('2##'+client.usr+'##'+client.toUsr+'##'+message,client.ADDR);
        #清空用户在Text中输入的消息
        self.textEdit.clear()

class IM_messageBoxImpl(QtWidgets.QDialog, Ui_messageBox):
    """QtGui.QWidget和界面设计时选择的类型一致"""
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self) # Ui_Form.setupUi


app = QtWidgets.QApplication(sys.argv)
ex = IM_loginDlgImpl()
ex2 = IM_FormImpl()
ex3 = IM_messageBoxImpl()
client = ClientMessage()

if __name__ == '__main__':

    ex.show()
    sys.exit(app.exec_())

