#encoding=utf-8
#使用tar zip归档文件
import  os
#将执行路径跳转到D盘
os.chdir("D:")
testdir="testfiveDir"
#判断所操作的路径地下是否存在testdir的路径
if not os.path.exists(testdir):
    os.mkdir(testdir)
os.chdir(testdir)
print "当前所在的文件位置：%s" % os.getcwd()
#创建文件
testfivefile="testfive.txt"
fivefile=open(testfivefile,"w")
fivefile.write("你好a\n")
fivefile.tell()
fivefile.write("你好a")
fivefile.tell()
fivefile.close()
fivefile=open(testfivefile,"r")
for eachline in fivefile:
    print eachline
fivefile.close()
#归档文件
import gzip
print "将文件:%s进行压缩" % testfivefile
fivefile=open(testfivefile,"rb")
z=gzip.open("file.txt.gz","wb")  #结尾为gz
z.writelines(fivefile)
z.close()
fivefile.close()
print "将文件:%s进行解压" % testfivefile
f = gzip.open('file.txt.gz', 'rb')
file_content = f.read()
f.close()
print file_content
#压缩
f=gzip.GzipFile("test.txt","wb",fileobj=open("test.gz","wb"))
f.write(open(testfivefile,"rb").read())
f.close()
#解压缩
g=gzip.GzipFile("","r",fileobj=open("test.gz","r"))
open(testfivefile, "wb").write(g.read())
print g.read()
# import tarfile
# t=tarfile.TarFile("",fileobj=open("test.tar.gz","w:gz"))
# t.add(open("test.gz","r"))
# t.close()
# for each in dir(zip("1,2,3,4","a,b,c,d")):
#     print each
