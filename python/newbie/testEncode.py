# coding:utf8
import os
import sys
print 123
print "哈哈"
print ("哈哈".decode("utf8").encode("gbk"))


data = raw_input("请输入：".decode("utf8").encode("gbk"))
# print (u"""哈哈""")

stdout_encode = sys.stdout.encoding #获取输出终端的编码方式
stdin_encode = sys.stdin.encoding
print stdout_encode
print stdin_encode
print (data)

if data.decode(stdin_encode).encode("utf8") == "哈哈":
    print "yoxi"



