# coding:utf8
# handling errors in python socket programs

# https://www.imooc.com/article/50566

import socket  # for sockets
import sys  # for exit
from time import ctime
import cchardet


def my_print(msg):
    stdout_encode = sys.stdout.encoding
    currentCode = cchardet.detect(msg)['encoding']
    return msg.decode(currentCode).encode(stdout_encode)


HOST = ''
PORT = 21567
BUFFERSIZE = 1024
ADDR = (HOST, PORT)

# create an AF_INET, STREAM socket (TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)
s.listen(5)
while True:
    print('waiting for connection...')
    tcpClient, addr = s.accept()
    print 'connected from:', addr
    while True:
        try:
            data = tcpClient.recv(BUFFERSIZE)

            print ("收到客户端的消息："), data.decode("gbk").encode("utf8")
            if not data:
                break
            data = ("[%s]%s" % (ctime(), data.decode("gbk").encode("utf8")))
            print "发送消息：", data
            tcpClient.send(bytes(data.decode("utf8").encode("gbk")))
        except Exception, e:
            print('关闭了正在占线的链接！')
            break
    tcpClient.close()
s.close()
print('x')
