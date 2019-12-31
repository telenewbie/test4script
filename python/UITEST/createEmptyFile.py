#encoding:utf-8
#这个文件用于自动生成文件
def createMp3File():
    for i in range(1000):
        filename=r"H:\music\音乐".decode("utf8").encode("gbk")+str(i)+".mp3"
        file=open(filename,"wb")
        file.close()

createMp3File()