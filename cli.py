# _*_ coding:utf-8 _*_
# Filename:ClientUI.py
# Python在线聊天客户端
from socket import *
import Tkinter
import tkFont
import socket
import thread
import time
import sys


reload(sys)
sys.setdefaultencoding( "utf-8" )


class ClientUI():
    
    title = 'Python在线聊天-客户端V1.0'
    local = '127.0.0.1'
    port = 8808
    global udpCliSock 
    buffer = 1024
    flag = False
    ADDR=(local,port)
    usr='12073128'
    pwd='12073128'
    toUsr='12073127'
    
    #初始化类的相关属性，类似于Java的构造方法
    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.title(self.title)
        
        #窗口面板,用4个面板布局
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
        self.sendButton.pack(expand=1,side=Tkinter.BOTTOM and Tkinter.RIGHT,padx=15,pady=8)
        #传文件按钮
        self.sendButton=Tkinter.Button(self.frame[3],text=' 传文件 ',width=10,command=self.sendFile)
        self.sendButton.pack(expand=1,side=Tkinter.BOTTOM and Tkinter.RIGHT,padx=15,pady=8)
        #关闭按钮
        self.closeButton=Tkinter.Button(self.frame[3],text=' 关 闭 ',width=10,command=self.close)
        self.closeButton.pack(expand=1,side=Tkinter.RIGHT,padx=15,pady=8)
        self.frame[3].pack(expand=1,fill=Tkinter.BOTH)
        
    #接收消息
    def receiveMessage(self):
        try:
            #建立Socket连接
            self.udpCliSock = socket.socket(AF_INET, SOCK_DGRAM)
            self.flag = True
        except:
            self.flag = False
            self.chatText.insert(Tkinter.END,'您还未与服务器端建立连接，请检查服务器端是否已经启动')
            return
       
        
        self.udpCliSock.sendto('0##'+self.usr+'##'+self.pwd,self.ADDR)
        while True:
            try:
                if self.flag == True:
                    #连接建立，接收服务器端消息
                    self.serverMsg ,self.ADDR  = self.udpCliSock.recvfrom(self.buffer)
                    s=self.serverMsg.split('##')
                    if s[0]=='Y':
                        self.chatText.insert(Tkinter.END,'客户端已经与服务器端建立连接......')
                    elif s[0]== 'N':
                        self.chatText.insert(Tkinter.END,'客户端与服务器端建立连接失败......')
                    elif s[0]=='0':
                        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        self.chatText.insert(Tkinter.END, theTime+' ' +'你的好友' + s[1]+'上线了')
                    elif s[0]=='1':
                        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        self.chatText.insert(Tkinter.END,  theTime +' '+s[1] +' 说：\n')
                        self.chatText.insert(Tkinter.END, '  ' + s[2])
                    elif s[0]=='2':
                        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        self.chatText.insert(Tkinter.END, theTime+' ' +'你的好友' + s[1]+'下线了')    
                    elif s[0]=='3':
                        filename=s[1]
                        fp = open(unicode('..\\'+self.usr+'\\'+filename[:-1] , "utf8"),'w')
                        fp.write(s[2])
                        fp.close()      
                        self.chatText.insert(Tkinter.END,filename[:-1]+' 传输完成')           
                else:
                    break
            except EOFError, msg:
                raise msg
                self.udpCliSock.close()
                break
                  
    #发送消息
    def sendMessage(self):
        #得到用户在Text中输入的消息
        message = self.inputText.get('1.0',Tkinter.END)
        #格式化当前的时间
        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.chatText.insert(Tkinter.END, theTime +'我' + ' 说：\n')
        self.chatText.insert(Tkinter.END,'  ' + message + '\n')
        if self.flag == True:
            #将消息发送到服务器端
            self.udpCliSock.sendto('1##'+self.toUsr+'##'+message+'##'+self.usr,self.ADDR);
        else:
            #Socket连接没有建立，提示用户
            self.chatText.insert(Tkinter.END,'您还未与服务器端建立连接，服务器端无法收到您的消息\n')
        #清空用户在Text中输入的消息
        self.inputText.delete(0.0,message.__len__()-1.0)
        
    #传文件
    def sendFile(self):
        filename = self.inputText.get('1.0',Tkinter.END)
        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.chatText.insert(Tkinter.END, theTime +'我' + ' 传文件：\n')
        self.chatText.insert(Tkinter.END,'  ' + filename[:-1] + '\n')
        fp = open('..\\'+self.usr+'\\'+filename[:-1],'r')
        filedata = fp.read(self.buffer)
       
        filedata =unicode(filedata,"utf8")
        self.udpCliSock.sendto('3##'+self.toUsr+'##'+self.usr+'##'+filename+'##'+filedata,self.ADDR);
        fp.close()
    #关闭消息窗口并退出
    def close(self):
        self.udpCliSock.sendto('2##'+self.usr,self.ADDR);
        sys.exit()
    
    #启动线程接收服务器端的消息
    def startNewThread(self):
        #启动一个新线程来接收服务器端的消息
        #thread.start_new_thread(function,args[,kwargs])函数原型，
        #其中function参数是将要调用的线程函数，args是传递给线程函数的参数，它必须是个元组类型，而kwargs是可选的参数
        #receiveMessage函数不需要参数，就传一个空元组
        thread.start_new_thread(self.receiveMessage,())

def main():
    client = ClientUI()
    client.startNewThread()
    client.root.mainloop()
    
if __name__=='__main__':
    main()
