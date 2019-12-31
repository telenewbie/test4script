# encoding=utf-8
import os
import threading
from time import sleep,ctime
import  json

#线程池
import threadpool

# for i, filename in enumerate(os.listdir("D:")):
#     if not isinstance(filename, unicode):
#         print i, filename.decode('gbk').encode('utf-8')  # 统一转成unicode编码，然后才可以进行编码，当前系统不支持gbk的输出

#数组
loops =[1,2,3]
threads = []
nloop = range(len(loops))

def loop(index,nsec):
    print index,"you sleep start ",nsec
    sleep(nsec)
    print index, "you sleep end ", nsec

def startTread():
    #打开线程
    for i in nloop:
        threads.append(threading.Thread(target=loop, args=(i, 5)))
    for i in nloop:
        threads[i].start()
    pass

def startPost():
    # 开始上传
    pass

def showFile(files):
    #输出每个文件
    for file in files:
        #如果后缀是wav则上传
        print file
    pass

def showFileTree():
    for root, dirs, files in os.walk(os.curdir, topdown=False):
        print "root", root.decode("gbk").encode("utf-8")
        print "dir", dirs
        showFile(files)



def showDir():
    pass


def waitAll():
    for i in nloop:
        threads[i].join()


def print_file_(filepath):
    print filepath

#startTread()

#等待所有的线程都完毕之后再输出
#waitAll()
#print_file_("D:")


class A(object):
    def __init__(self):
        pass
    def __del__(self):
        pass

class B(object):
    pass
class C1(A,B):
    pass
class C2(A,B):
    pass
class GC(C1,C2):
    pass
print GC.__mro__

#



def startThreadPool():
    name_list = [(['caoshuai', 1], None), (['caoshuai', 2], None), (['a', 3], None), (['ss', 4], None),
                 (['wwwwww', 12], None),
                 (['m', 12], None), (['n', 12], None), (['b', 12], None), (['v', 12], None), (['x', 12], None),
                 (['z', 12], None), ]

    pool = threadpool.ThreadPool(10)
    requestss = threadpool.makeRequests(loop, name_list)

    [pool.putRequest(req) for req in requestss]

    pool.wait()


jsonStr = '{"state": "OK", "code": 0, "result": {"text": "小杜小杜", "code": 1}}'

text = json.loads(jsonStr)

print text['state']
print text['code']
print text['result']['text']
print text['result']['code']
print "finish"
