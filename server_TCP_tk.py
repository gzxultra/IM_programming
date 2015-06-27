# _*_ coding:utf-8 _*_
# Filename:ServerUI.py
# Python在线聊天服务器端

import Tkinter
import tkFont
import socket
import thread
import time
import sys
import os
import SocketServer
import threading

local = '127.0.0.1'
port = 8808
ADDR = (local,port)
class ServerUI():


    title = 'Python在线聊天-服务器端V1.0'

    global tcpSerSock
    flag = False
    global addr
    global usr_online

    #初始化类的相关属性，类似于Java的构造方法
    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.title(self.title)

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


    #发送消息
    def sendMessage(self):
        #得到用户在Text中输入的消息
        message = self.inputText.get('1.0',Tkinter.END)
        #格式化当前的时间
        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.chatText.insert(Tkinter.END, '服务器 ' + theTime +' 说：\n')
        self.chatText.insert(Tkinter.END,'  ' + message + '\n'+str(self.addr))

            #将消息发送到客户端
        self.tcpSerSock.send(message)

        #清空用户在Text中输入的消息
        self.inputText.delete(0.0,message.__len__()-1.0)


    #关闭消息窗口并退出
    def close(self):
        sys.exit()

    #启动线程接收客户端的消息
    def startNewThread(self):
        # Run server
        server = ThreadedTCPServer(ADDR,ThreadedTCPRequestHandler)
        ip, port = server.server_address

        self.chatText.insert(Tkinter.END,'服务器已经就绪......')
        # Start a new thread when with the server, -- one thread per request
        server_thread = threading.Thread(target = server.serve_forever)
        # Exit the server thread when the main thread exits
        server_thread.daemon = True
        server_thread.start()




class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.usr_online = []
        clientMsg = self.request.recv(1024)

        s = clientMsg.split('##')

        if s[0]=='0':
            fobj=open('usr&pwd.txt','r')
            for eachLine in fobj:
                if eachLine.split(' ')[0]==s[1] and eachLine.split(' ')[1]==s[2]:
                    serverUI.chatText.insert(Tkinter.END,'服务器端已经与客户端建立连接......',self.client_address)
                    #发送好友上线信息
                    for each in self.usr_online:
                        self.request.send('0##'+s[1])

                    mark = 1
                    #添加到上线用户列表
                    self.usr_online.append([s[1],self.client_address])
                    self.request.send('Y')
                    break
            fobj.close()
            if mark==0:
                serverUI.chatText.insert(Tkinter.END,'服务器端与客户端建立连接失败......')
                self.request.send('N',self)
        elif s[0]=='1':
            for each in self.usr_online:
                if s[1] == each[0]:
                    self.request.send('1##'+s[3]+'##'+s[2])
                    break
            theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            serverUI.chatText.insert(Tkinter.END, theTime +' 客户端 ' +s[3] +' 对 客户端 ' + s[1] +' 说：\n')
            serverUI.chatText.insert(Tkinter.END, '  ' + s[2]+str(each[1]))
        elif s[0]=='2':
            self.usr_online= filter(lambda x:x !=[s[1],self.addr],self.usr_online)
            for each in self.usr_online:
                self.request('3##'+s[1])

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__=='__main__':
    serverUI = ServerUI()
    serverUI.startNewThread()
    serverUI.root.mainloop()