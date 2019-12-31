#coding=utf8

# 读取文件，然后在后面增加一秒钟的静音超时
# r w a / t b
import sys
import os


def __code(s, src, target):
    u = ''
    while True:
        try:
            u = s.decode(src)   #1可能抛异常，也可能不抛异常
        except (UnicodeDecodeError, e):  #如果s是target编码，转成unicode失败，抛此异常
            #print repr(e)
            break
        except (UnicodeEncodeError, e):#如果s是unicode编码，转成unicode失败，抛此异常
            #print repr(e)
            u = s
        try:
            s = u.encode(target)
        except (Exception, e):
            break
        break
    return s


def utf8(s):
    return __code(s, 'gbk', 'utf8')


def gbk(s):
    return __code(s, 'utf8', 'gbk')


def readfile(filename):
    with open(filename, 'r') as f:
        print(f.readline().strip())  # 去掉回车换行


def append_data2file(str):
    with open('suffix.pcm', 'rb') as f:
        with open(str, "ab+") as fw:
            fw.write(f.read())


# 先使用原有的进行覆盖吧
# 文件还原
def undo():
    with open('wifi1.pcm', 'rb') as f:
        with open('wifi.pcm', "wb") as fw:
            fw.write(f.read())


def cycle_file(path):
    g = os.walk(path)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            print(utf8(os.path.join(path, file_name)))  # utf 的格式打印
            if file_name[-4::] == '.pcm':
                append_data2file(os.path.join(path, file_name))


if __name__ == '__main__':
    cycle_file(".")
    # cycle_file("C:\\Users\\telenewbie\\Desktop\\voice")