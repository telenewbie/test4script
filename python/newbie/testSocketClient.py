# ecoding:utf-8

# 创建客户端
from socket import *

HOST = 'localhost'
PORT = 21567
BUFFERSIZE = 1024
ADDR = (HOST, PORT)

tcpClient = socket(AF_INET, SOCK_STREAM)
tcpClient.connect(ADDR)
while True:
    data = input("请输入:")
    if not data:
        break
    tcpClient.send(bytes(data.decode('utf-8').encode('gbk')))
    tcpClient.recv(BUFFERSIZE)
    if not data:
        break
    print(data)
tcpClient.close()
