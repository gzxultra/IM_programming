# _*_ coding:utf-8 _*_
# Filename:ServerUI.py
# Python在线聊天服务器端
from socket import *
import socket
import Tkinter
import tkFont
import thread
import time
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class ServerMessage():
    #设置标题
    def setTitle(self,title):
        self.title=title
    
    #设置ip地址和端口号
    def setLocalANDPort(self,local,port):
        self.local = local
        self.port = port
        
    def __init__(self,title):
        self.root = Tkinter.Tk()
        self.root.title(title)
        
        #窗口面板,用4个frame面板布局
        self.frame = [Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame()]

        #显示消息Text右边的滚动条
        self.chatTextScrollBar = Tkinter.Scrollbar(self.frame[0])
        self.chatTextScrollBar.pack(side=Tkinter.RIGHT,fill=Tkinter.Y)
        
        #显示消息Text，并绑定上面的滚动条
        ft = tkFont.Font(family='Fixdsys',size=11)
        self.chatText = Tkinter.Listbox(self.frame[0],width=70,height=18,font=ft)
        self.chatText['yscrollcommand'] = self.chatTextScrollBar.set
        self.chatText.pack(expand=1,fill=Tkinter.BOTH)
        self.chatTextScrollBar['command'] = self.chatText.yview()
        self.frame[0].pack(expand=1,fill=Tkinter.BOTH)
        
        #标签，分开消息显示Text和消息输入Text
        label = Tkinter.Label(self.frame[1],height=2)
        label.pack(fill=Tkinter.BOTH)
        self.frame[1].pack(expand=1,fill=Tkinter.BOTH)
        
        #输入消息Text的滚动条
        self.inputTextScrollBar = Tkinter.Scrollbar(self.frame[2])
        self.inputTextScrollBar.pack(side=Tkinter.RIGHT,fill=Tkinter.Y)
        
        #输入消息Text，并与滚动条绑定
        ft = tkFont.Font(family='Fixdsys',size=11)
        self.inputText = Tkinter.Text(self.frame[2],width=70,height=8,font=ft)
        self.inputText['yscrollcommand'] = self.inputTextScrollBar.set
        self.inputText.pack(expand=1,fill=Tkinter.BOTH)
        self.inputTextScrollBar['command'] = self.chatText.yview()
        self.frame[2].pack(expand=1,fill=Tkinter.BOTH)
        
        #发送消息按钮
        self.sendButton=Tkinter.Button(self.frame[3],text=' 发 送 ',width=10,command=self.sendMessage)
        self.sendButton.pack(expand=1,side=Tkinter.BOTTOM and Tkinter.RIGHT,padx=25,pady=5)
        


        #关闭按钮
        self.closeButton=Tkinter.Button(self.frame[3],text=' 关 闭 ',width=10,command=self.close)
        self.closeButton.pack(expand=1,side=Tkinter.RIGHT,padx=25,pady=5)
        self.frame[3].pack(expand=1,fill=Tkinter.BOTH)
        
    #接收消息
    def receiveMessage(self):
        self.usr_sum=0
        self.usr_online = []
        self.ADDR = (self.local,self.port)
        #建立Socket连接
        self.udpSerSock = socket.socket(AF_INET, SOCK_DGRAM)
        self.udpSerSock.bind(self.ADDR)
        self.buffer = 1024
        self.chatText.insert(Tkinter.END,'服务器已经就绪......')
        #循环接受客户端的连接请求
        
        while True:
            mark=0
            isOnline=0
            self.clientMsg, self.addr = self.udpSerSock.recvfrom(self.buffer)
            s=self.clientMsg.split('##')
            #收到上线信号
            if s[0]=='0':
                fobj=open('usr&pwd.txt','r')
                for eachLine in fobj:
                    if eachLine.split(' ')[0]==s[1] and eachLine.split(' ')[1]==s[2]:
                        self.chatText.insert(Tkinter.END,'服务器端已经与客户端建立连接......'+str(self.addr))
                        self.udpSerSock.sendto('Y',self.addr)
                        
                        #检查是否已登录，将原登陆客户端退出并抹去在线用户列表中的
                        for each in self.usr_online:
                            if s[1]==each[0]:
                                self.udpSerSock.sendto('CLOSE',each[1])
                                self.usr_online= filter(lambda x:x !=[s[1],each[1]],self.usr_online)
                                isOnline=1
                                break
                        #检查是否有离线消息
                        fp = open(unicode(s[1]+'.txt', "utf8"),'r+')
                        temp=''
                        for eachLine1 in fp:
                            if eachLine1[0]=='2':
                                self.udpSerSock.sendto(temp,self.addr)
                                temp=eachLine1
                            else :
                                temp=temp+eachLine1
                        self.udpSerSock.sendto(temp,self.addr)
                        #清空文件内容
                        fp.truncate(0)
                        fp.close() 
                        #发送好友上线信息
                        if isOnline==0:
                            for each in self.usr_online:
                                self.udpSerSock.sendto('0##'+s[1],each[1])
                            #添加到上线用户列表
                        self.usr_online.append([s[1],self.addr])
                        mark=1                       
                        break
                fobj.close()
                if mark==0:
                    self.chatText.insert(Tkinter.END,'服务器端与客户端建立连接失败......')
                    self.udpSerSock.sendto('N',self.addr)
            #收到下线信号
            elif s[0]=='1':
                self.usr_online= filter(lambda x:x !=[s[1],self.addr],self.usr_online)
                for each in self.usr_online:
                    self.udpSerSock.sendto('1##'+s[1],each[1])
            #收到消息
            elif s[0]=='2':
                toUsrIsOnline=0
                for each in self.usr_online:
                    if s[2]==each[0]:
                        self.udpSerSock.sendto(self.clientMsg,each[1])
                        toUsrIsOnline=1
                        break
                if toUsrIsOnline==0:
                    fp = open(unicode(s[2]+'.txt', "utf8"),'a')
                    fp.write(self.clientMsg)
                    fp.close()    
                    
                theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                self.chatText.insert(Tkinter.END, theTime +' 客户端 ' +s[1] +' 对 客户端 ' + s[2] +' 说：\n')
                self.chatText.insert(Tkinter.END, '  ' + s[3]+str(each[1]))
            #收到文件
            elif s[0]=='3':
                    for each in self.usr_online:
                        if s[2]==each[0]:
                            self.udpSerSock.sendto('3##'+s[1]+'##'+s[3],each[1])
                            break

    #发送消息
    def sendMessage(self):
        usrIsOnline=0
        #得到用户在Text中输入的消息
        
        message = self.inputText.get('1.0',Tkinter.END)
        s=message.split('##')
        
        #格式化当前的时间
        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for each in self.usr_online:
            if s[0]==each[0]:
                self.udpSerSock.sendto('2##服务器##'+s[0]+'##'+s[1],each[1])
                usrIsOnline=1
                self.chatText.insert(Tkinter.END, '服务器 ' + theTime +' 对 '+s[0]+' 说：\n')
                self.chatText.insert(Tkinter.END,'  ' + s[1] + '\n')
                break
        if usrIsOnline==0:
            self.chatText.insert(Tkinter.END, '用户'+s[0]+'不在线\n')

        #清空用户在Text中输入的消息
        self.inputText.delete(0.0,message.__len__()-1.0)
    
    #关闭消息窗口并退出
    def close(self):
        sys.exit()
    
    #启动线程接收客户端的消息
    def startNewThread(self):
        thread.start_new_thread(self.receiveMessage,())
    
def main():
    server = ServerMessage('服务端')
    server.setLocalANDPort('192.168.1.105',8808)
    server.startNewThread()
    server.root.mainloop()
    
    
if __name__=='__main__':
    main()
