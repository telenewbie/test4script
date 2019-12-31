# coding:utf8
# 字符编码 采用 cchardet 进行detect 来获取
# "请输入：".decode(currentCode).encode(stdout_encode) 在任意地平台都可以使用

import os
import sys
import cchardet
print 123
print "哈哈"
print u"哈哈"
print ("哈哈".decode("utf8").encode("gbk"))

def my_print(msg):
    stdout_encode = sys.stdout.encoding
    currentCode = cchardet.detect(msg)['encoding']
    return msg.decode(currentCode).encode(stdout_encode)

# data = raw_input("请输入：".decode("utf8").encode("gbk"))
# print (u"""哈哈""")

stdout_encode = sys.stdout.encoding #获取输出终端的编码方式
stdin_encode = sys.stdin.encoding
currentCode = cchardet.detect("哈哈")['encoding']  # 检测当前的字符编码
data = raw_input("请输入：".decode(currentCode).encode(stdout_encode))
print stdout_encode
print stdin_encode
print (data)

if data.decode(stdin_encode).encode("utf8") == "哈哈":
    print "yoxi"



