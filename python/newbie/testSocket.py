# handling errors in python socket programs

import socket  # for sockets
import sys  # for exit
from time import ctime

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
    print 'connected from:' , addr
    while True:
        data = tcpClient.recv(BUFFERSIZE)
        if not data:
            break
        tcpClient.send("[%s]%s" % (ctime(), data))
    tcpClient.close()
s.close()
print('x')
