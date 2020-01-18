# encoding=utf-8
from __future__ import with_statement


def test():
    print  "你好"

    try:
        # with [for i in range(10)]as k:
        #     print k
        # assert 1==0
        raise SyntaxError("cuowu")
    except SyntaxError, e:
        import sys

        exc_tuple = sys.exc_info()
        for eachItem in exc_tuple:
            print eachItem
        print e
    else:
        print "else"
    finally:
        print "finally"
    import os

    print "11", os.altsep, "xxx"
    print os.getcwd()
    os.chdir("d:")
    print os.getcwd()
    import sys

    print sys.getdefaultencoding()

    for i, filename in enumerate(os.listdir(os.getcwd())):
        if not isinstance(filename, unicode):
            print i, filename.decode('gbk').encode('utf-8')  # 统一转成unicode编码，然后才可以进行编码，当前系统不支持gbk的输出


# 使用os和os.path进行一系列的操作之后退出
def code(str):
    if not isinstance(str, unicode):
        str.decode("gbk").encode("utf8")
    else:
        str.encode('utf8')


def deleteTree(src):
    os.removedirs(src)

testfileDir = 'testpython'
testfilename = "testpython.txt"
dirName = "中文名称文件".decode("utf8").encode("gbk")
import os
import sys
def testos():
    # try:
    os.chdir("D:")
    print "当前所在的位置：", os.getcwd()
    if not os.path.exists(testfileDir):
        os.mkdir(testfileDir)
    os.chdir(testfileDir)
    print "创建之后，当前所在的位置：", os.getcwd()
    f = open(testfilename, "w")
    hello = '你好'
    f.write(hello)
    f.write(os.linesep)
    f.write("hello")
    f.flush()
    f.close()
    print "对文件进行操作完毕"
    f = open(testfilename, "r")
    for eachline in f:
        print eachline
    f.close()
    print "文件的内容读取完毕"

    if not os.path.exists(dirName):
        os.mkdir(dirName)
    for filename in os.listdir(os.getcwd()):
        print filename.decode("gbk").encode("utf-8")
    print "读取文件目录完毕"
    # os.rename(testfilename, "test.ttt")
    allpath = os.path.join(os.getcwd(), "test.ttt")
    print "完整的路径名称是：", allpath
    print "执行 splitext:", os.path.splitext(allpath)
    print "执行 basename:", os.path.basename(allpath)
    print "执行 expanduser:", os.path.expanduser(allpath)
    print "执行 expandvars:", os.path.expandvars(allpath)
    print "执行 dirname:", os.path.dirname(allpath)
    # 生成一个目录下的所有文件（包括文件夹和文件）
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        print "root", root.decode("gbk").encode("utf-8")
        print "dir", dirs
        print "file",files
    print "开始删除文件和文件夹"
    # os.chdir(os.path.dirname(allpath))
    os.remove(allpath)
    print os.listdir(os.getcwd())

    os.chdir(os.pardir)         #上一级目录
    #此种方式部分中英文全部删除
    # import shutil
    # shutil.rmtree(testfileDir)
    # os.removedirs(testfileDir)
    print os.getcwd()
    # os.remove(os.path.dirname(allpath))
    finalFile = testfileDir + os.sep + dirName
    deleteTree(finalFile)


    print "删除完成"
    # except Exception,e:
    #     print e.message
    #     if os.path.exists("test.ttt"):
    #         os.remove("test.ttt")

test()
testos()

