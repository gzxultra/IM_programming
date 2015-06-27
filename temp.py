    #接收消息
    def receiveMessage(self):
        self.usr_online = []
        #建立Socket连接
        self.tcpSerSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcpSerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpSerSock.bind(self.ADDR)
        self.tcpSerSock.listen(15)
        self.buffer = 1024
        self.chatText.insert(Tkinter.END,'服务器已经就绪......')

        self.startNewThread()

        #循环接受客户端的连接请求
        while True:
            mark = 0
            self.tcpSerSock,self.addr = self.tcpSerSock.accept()
            self.flag = True

            while True:
                #接收客户端发送的消息
                self.clientMsg = self.tcpSerSock.recv(self.buffer)
                if not self.clientMsg:
                    continue
                s=self.clientMsg.split('##')
                if s[0]=='0':
                    fobj=open('usr&pwd.txt','r')
                    for eachLine in fobj:
                        if eachLine.split(' ')[0]==s[1] and eachLine.split(' ')[1]==s[2]:
                           serverUI.chatText.insert(Tkinter.END,'服务器端已经与客户端建立连接......'+str(self.addr))
                            #发送好友上线信息
                            for each in self.usr_online:
                                self.tcpSerSock.send('0##'+s[1])
                            mark = 1
                            #添加到上线用户列表
                            self.usr_online.append([s[1],self.addr])
                            self.tcpSerSock.send('Y')
                            break
                    fobj.close()
                    if mark==0:
                        self.chatText.insert(Tkinter.END,'服务器端与客户端建立连接失败......')
                        self.tcpSerSock.send('N',self)
                elif s[0]=='1':
                    for each in self.usr_online:
                        if s[1] == each[0]:
                            self.tcpSerSock.send('1##'+s[3]+'##'+s[2])
                            break
                    theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    self.chatText.insert(Tkinter.END, theTime +' 客户端 ' +s[3] +' 对 客户端 ' + s[1] +' 说：\n')
                    self.chatText.insert(Tkinter.END, '  ' + s[2]+str(each[1]))
                elif s[0]=='2':
                    self.usr_online= filter(lambda x:x !=[s[1],self.addr],self.usr_online)
                    for each in self.usr_online:
                        self.tcpSerSock('3##'+s[1])
