# coding:utf-8
# 这个脚本是用来杀掉music的进程的
import os
import string
import subprocess


def kill(result):
    print result.strip()
    code = os.system(" adb shell kill " + result.strip())
    print code

print '-'*20
processname = os.system('''adb shell ps|grep com.txznet.music|awk '{print$2","}''''')
# 这里执行报错的原因是 grep不是连在 adb shell 的环境里面进行 的操作，还是再windows里面
print '-'*20
# print processname
# result="["+str(processname)+"]"
# print result
# for processID in result:
#     print processID.strip()
#     code=os.system(" adb shell kill "+processID.strip())
#     print code
print '-'*20
result = subprocess.Popen("""adb shell ps|grep com.txznet.music|awk '{print $2}'""", stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE)
print '-'*20
stdout, stderr = result.communicate()
print '-'*20
print stdout.decode("gbk").encode("utf-8")
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
