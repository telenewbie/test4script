# coding:utf-8

import subprocess
from threading import Timer
import ctypes
import sys

# 1.
# ftest1=subprocess.Popen('adb shell cd sdcard/Android/data &&ls',stdout=subprocess.PIPE, stderr=subprocess.PIPE) #使用&&来进行连续的操作
# print ftest1.stdout.read()

# 2.
cmds = [
'pm uninstall com.txznet.music',
'exit',
        ]

p = subprocess.Popen(['adb shell'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

cmds='\n'.join(cmds)+'\n'
print cmds
outstr, errstr = p.communicate(cmds)
print outstr
# import subprocess
# child1 = subprocess.Popen("adb shell", stdout=subprocess.PIPE)
# child2 = subprocess.Popen("ls",stdin=child1.stdout, stdout=subprocess.PIPE)
# out = child2.communicate()
# print out

# 测试几个类
# import ctypes
#
# print ctypes.windll.kernel32.CreateToolhelp32Snapshot
#
# print ctypes.windll
# print (ctypes.windll)
