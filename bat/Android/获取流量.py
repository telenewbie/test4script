#!/usr/bin/env python
#coding=utf-8
import os
import string
import subprocess
import sys

# line=os.system('adb shell dumpsys package com.txznet.music |findstr userId ')
# newline= "",line,""
# print newline[:]

def getCurrentUID():
    pipe = subprocess.Popen("adb shell dumpsys package com.txznet.music |grep 'userId' ", stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    result = pipe.stdout.readline()
    trimUids=string.strip(result)
    lastindex=trimUids.index(" ")
    uid= trimUids[7:lastindex]
    return uid

def getCurrentflow(uid):
    pipe = subprocess.Popen("adb shell cat /proc/net/xt_qtaguid/stats | grep  "+uid, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    results=pipe.stdout.readlines()
    count =0
    for result in results:
        value=result.split(" ")
        count+=(int(value[5])+int(value[7]))

    sum=count*1.0/1024/1024

    return sum

def subtractFlow(uid):
    lastsum=getCurrentflow(uid)
    raw_input("watting util finish your second flow...")
    return (getCurrentflow(uid)-lastsum)


def conslone():
    uid=getCurrentUID()
    while True:
        input=raw_input("""
        \t\t\t查看流量的程序\t\t\t\n
         1.查看当前的uid
         2.查看当前的流量消耗
         3.查看两次的流量消耗
        """.decode('utf-8').encode('gbk'))
        if input =="0":
            break
        elif input =="1":
            uid=getCurrentUID()
            print uid
        elif input=="2":
            print getCurrentflow(uid)
        elif input=="3":
            print subtractFlow(uid)


def printChinese(s):
    if isinstance(s, unicode): 
    #s=u"中文" 
        print s.encode('gb2312') 
    else: 
    #s="中文" 
        print s.decode('utf-8').encode('gb2312')
print sys.getdefaultencoding()
print u"我是中文"
printChinese("中文")
conslone()

os.system("pause")

