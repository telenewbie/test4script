# coding:utf-8
# 这个脚本是用来杀掉music的进程的
import os
import string
import subprocess


def kill(result):
    print result.strip()
    code = os.system(" adb shell kill " + result.strip())
    print code


processname = os.system('''adb shell ps|grep com.txznet.music|awk '{print$2","}''''')

# print processname
# result="["+str(processname)+"]"
# print result
# for processID in result:
#     print processID.strip()
#     code=os.system(" adb shell kill "+processID.strip())
#     print code

result = subprocess.Popen("""adb shell ps|grep com.txznet.music|awk '{print $2}'""", stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE)

stdout, stderr = result.communicate()
print stdout
for processID in stdout.splitlines():
    print processID.strip()
    if len(processID.strip()) > 0:
        print os.popen(" adb shell kill " + processID.strip())
        # print code

# result=pipe.communicate("ps|grep com.txznet.music|awk '{print$2","}'")
# print result
# result = pipe.stdout.readline()
# result1 = pipe.stdout.readline()
# result2 = pipe.stdout.readline()
# print result
# kill(result)
# print result1
# kill(result1)
# print result2
# kill(result2)
