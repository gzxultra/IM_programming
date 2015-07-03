# _*_ coding:utf-8 _*_
# Filename:ClientUI.py
# Python在线聊天客户端
from socket import *
from ftplib import FTP
import ftplib
import Tkinter
import tkFont
import socket
import thread
import time
import sys
import codecs
import time
import os
reload(sys)
sys.setdefaultencoding( "utf-8" )

class ClientUI():
    
    usr='12073128'
    pwd='12073128'

    title = usr+'客户端'
    
    local = '192.168.1.105'
    port = 8808
    ADDR=(local,port)
    #global udpCliSock    1
     
    buffer = 1024

    
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
        self.sendButton=Tkinter.Button(self.frame[3],text='发 送 ',width=10,command=self.sendMessage)
        self.sendButton.pack(expand=1,side=Tkinter.BOTTOM and Tkinter.RIGHT,padx=15,pady=8)
        #传文件按钮
        self.sendButton=Tkinter.Button(self.frame[3],text='传文件 ',width=10,command=self.sendFile)
        self.sendButton.pack(expand=1,side=Tkinter.BOTTOM and Tkinter.RIGHT,padx=15,pady=8)
        #加好友按钮
        self.sendButton=Tkinter.Button(self.frame[3],text='加好友',width=10,command=self.addFriends)
        self.sendButton.pack(expand=1,side=Tkinter.BOTTOM and Tkinter.RIGHT,padx=15,pady=8)
        #目标好友按钮
        self.sendButton=Tkinter.Button(self.frame[3],text='选择好友',width=10,command=self.setTOusr)
        self.sendButton.pack(expand=1,side=Tkinter.BOTTOM and Tkinter.RIGHT,padx=15,pady=8)
        #关闭按钮
        self.closeButton=Tkinter.Button(self.frame[3],text='关闭 ',width=10,command=self.close)
        self.closeButton.pack(expand=1,side=Tkinter.RIGHT,padx=15,pady=8)
        self.frame[3].pack(expand=1,fill=Tkinter.BOTH)
        
    #接收消息
    def receiveMessage(self):
        self.udpCliSock = socket.socket(AF_INET, SOCK_DGRAM)
        self.udpCliSock.sendto('0##'+self.usr+'##'+self.pwd,self.ADDR)
  
        while True:
            #连接建立，接收服务器端消息
            self.serverMsg ,self.ADDR  = self.udpCliSock.recvfrom(self.buffer)
            s=self.serverMsg.split('##')
            if s[0]=='Y':
                self.chatText.insert(Tkinter.END,'客户端已经与服务器端建立连接......')
            elif s[0]== 'N':
                self.chatText.insert(Tkinter.END,'客户端与服务器端建立连接失败......')
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
                #如果s[3]为'Y'弹出框，显示s[2]添加成功，用户点击确认即可
                    #刷新好友列表
                #如果s[3]为'N'弹出框，显示s[2]添加失败，用户点击确认即可
                
                  
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
        self.inputText.delete(0.0,filename.__len__()-1.0)
    #加好友
    def addFriends(self):
        message= self.inputText.get('1.0',Tkinter.END)
        s=message.split('##')
        self.udpCliSock.sendto('4##'+self.usr+'##'+s[0]+'##'+s[1],self.ADDR);
    def setTOusr(self):
        self.toUsr=self.inputText.get('1.0',Tkinter.END)[:-1]
        self.title = self.usr+'-to-'+self.toUsr+'  客户端'
        self.root.title(self.title)
        

    #关闭消息窗口并退出
    def close(self):
        self.udpCliSock.sendto('1##'+self.usr,self.ADDR);
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
