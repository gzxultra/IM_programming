
# _*_ coding:utf-8 _*_
# Filename:ClientUI.py
# Python在线聊天客户端
from socket import *
from ftplib import FTP
import ftplib
import socket
import thread
import time
import sys
import codecs
import os
reload(sys)
sys.setdefaultencoding( "utf-8" )

class ClientMessage():
    #设置用户名密码
    def setUsrANDPwd(self,usr,pwd):
        self.usr=usr
        self.pwd=pwd

    #设置目标用户
    def setToUsr(self,toUsr):
        self.toUsr=toUsr
        self.ChatFormTitle=toUsr

    #设置ip地址和端口号
    def setLocalANDPort(self,local,port):
        self.local = local
        self.port = port

    def check_info(self):
        self.buffer = 1024
        self.ADDR=(self.local,self.port)
        self.udpCliSock = socket.socket(AF_INET, SOCK_DGRAM)
        self.udpCliSock.sendto('0##'+self.usr+'##'+self.pwd,self.ADDR)
        self.serverMsg ,self.ADDR  = self.udpCliSock.recvfrom(self.buffer)

        s=self.serverMsg.split('##')
        if s[0]=='Y':
            return True
        elif s[0]== 'N':
            return False

    #接收消息
    def receiveMessage(self):
        self.buffer = 1024
        self.ADDR=(self.local,self.port)
        self.udpCliSock = socket.socket(AF_INET, SOCK_DGRAM)
        self.udpCliSock.sendto('0##'+self.usr+'##'+self.pwd,self.ADDR)

        while True:
            #连接建立，接收服务器端消息
            self.serverMsg ,self.ADDR  = self.udpCliSock.recvfrom(self.buffer)
            s=self.serverMsg.split('##')
            if s[0]=='Y':
                #self.chatText.insert(Tkinter.END,'客户端已经与服务器端建立连接......')
                return True
            elif s[0]== 'N':
                #self.chatText.insert(Tkinter.END,'客户端与服务器端建立连接失败......')
                return False
            elif s[0]=='CLOSE':
                i=5
                while i>0:
                    self.chatText.insert(Tkinter.END,'你的账号在另一端登录，该客户端'+str(i)+'秒后退出......')
                    time.sleep(1)
                    i=i-1
                    self.chatText.delete(Tkinter.END)
                os._exit(0)
           #好友列表
           elif s[0]=='F':
                for eachFriend in s[1:len(s)]:
                    print eachFriend
            #好友上线
            elif s[0]=='0':
                theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                self.chatText.insert(Tkinter.END, theTime+' ' +'你的好友' + s[1]+'上线了')
            #好友下线
            elif s[0]=='1':
                theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                self.chatText.insert(Tkinter.END, theTime+' ' +'你的好友' + s[1]+'下线了')
            #好友传来消息
            elif s[0]=='2':
                theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                self.chatText.insert(Tkinter.END,  theTime +' '+s[1] +' 说：\n')
                self.chatText.insert(Tkinter.END, '  ' + s[3])
            #好友传来文件
            elif s[0]=='3':
                filename=s[2]
                f=FTP('192.168.1.105')
                f.login('Coder', 'xianjian')
                f.cwd(self.usr)
                filenameD=filename[:-1].encode("cp936")
                try:
                    f.retrbinary('RETR '+filenameD,open('..\\'+self.usr+'\\'+filenameD,'wb').write)
                except ftplib.error_perm:
                    print 'ERROR:cannot read file "%s"' %file
                self.chatText.insert(Tkinter.END,filename[:-1]+' 传输完成')
            elif s[0]=='4':
                agreement=raw_input(s[1]+'请求加你为好友，验证消息:'+s[3]+'你愿意加'+s[1]+'为好友吗(Y/N)')
                if agreement=='Y':
                    self.udpCliSock.sendto('5##'+s[1]+'##'+s[2]+'##Y',self.ADDR)
                elif agreement=='N':
                    self.udpCliSock.sendto('5##'+s[1]+'##'+s[2]+'##N',self.ADDR)
            elif s[0]=='5':
                if s[3]=='Y':
                    print s[2]+'接受了你的好友请求'
                elif s[3]=='N':
                    print s[2]+'拒绝了你的好友请求'
    #发送消息
    def sendMessage(self):
        #得到用户在Text中输入的消息
        message = self.inputText.get('1.0',Tkinter.END)
        #格式化当前的时间
        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.chatText.insert(Tkinter.END, theTime +' 我 说：\n')
        self.chatText.insert(Tkinter.END,'  ' + message + '\n')
        self.udpCliSock.sendto('2##'+self.usr+'##'+self.toUsr+'##'+message,self.ADDR);
        #清空用户在Text中输入的消息
        self.inputText.delete(0.0,message.__len__()-1.0)



    #传文件
    def sendFile(self):
        filename = self.inputText.get('1.0',Tkinter.END)
        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.chatText.insert(Tkinter.END, theTime +'我' + ' 传文件：\n')
        self.chatText.insert(Tkinter.END,'  ' + filename[:-1] + '\n')
        f=FTP('192.168.1.105')
        f.login('Coder', 'xianjian')
        f.cwd(self.toUsr)
        filenameU=filename[:-1].encode("cp936")
        try:
            #f.retrbinary('RETR '+filename,open(filename,'wb').write)
            #将文件上传到服务器对方文件夹中
            f.storbinary('STOR ' + filenameU, open('..\\'+self.usr+'\\'+filenameU, 'rb'))
        except ftplib.error_perm:
            print 'ERROR:cannot read file "%s"' %file
        self.udpCliSock.sendto('3##'+self.usr+'##'+self.toUsr+'##'+filename,self.ADDR);

    #加好友
    def addFriends(self):
        message= self.inputText.get('1.0',Tkinter.END)
        s=message.split('##')
        self.udpCliSock.sendto('4##'+self.usr+'##'+s[0]+'##'+s[1],self.ADDR);

    #关闭消息窗口并退出
    def close(self):
        self.udpCliSock.sendto('1##'+self.usr,self.ADDR);
        sys.exit()

    #启动线程接收服务器端的消息
    def startNewThread(self):
        thread.start_new_thread(self.receiveMessage,())

def main():
    client = ClientMessage()
    client.setLocalANDPort('192.168.1.105', 8808)
    client.setUsrANDPwd('12073127', '12073127')
    client.setToUsr('12073128')
    client.startNewThread()

if __name__=='__main__':
    main()

