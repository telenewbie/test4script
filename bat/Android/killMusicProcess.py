# coding:utf-8
# 这个脚本是用来杀掉music的进程的
import os
import string
import subprocess
import sys

if (len(sys.argv)>1):
    processName=sys.argv[1]
else:
    processName="com.txznet.music"

def kill(result):
    # print result.strip()
    code = os.system(" adb shell kill " + result.strip())
    # print code

processname = os.system('''adb shell ps|grep '''+processName+'''|awk '{print$2","}''''')


# print processname
# result="["+str(processname)+"]"
# print result
# for processID in result:
#     print processID.strip()
#     code=os.system(" adb shell kill "+processID.strip())
#     print code

pipe = subprocess.Popen("adb shell ps|grep "+processName+"|awk '{print$2}'", stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE)

# result=pipe.communicate("ps|grep com.txznet.music|awk '{print$2","}'")
# print result
result = pipe.stdout.readline()
# result1 = pipe.stdout.readline()
# result2 = pipe.stdout.readline()
if(result != ""):
	kill(result)
else:
    print "没有相关进程"
# print result1
# kill(result1)
# print result2
# kill(result2)

