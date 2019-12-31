# coding:utf-8
# 这个脚本用于使环境拥有busybox的环境
import subprocess

import os
print "开始push文件"
os.system(" adb push busybox /system/xbin/")
print "开始root"
os.system("adb root")
print "开始remote"
os.system("adb remount")

cmds = [
    "chmod  755 /system/xbin/busybox",
    "cd /system/xbin",
    "busybox --install .",
    "awk",
    "ps |grep com.txznet.music|awk '{print $2}' | head -n 1",
    "exit",#这是是非常关键的，退出
]
print "开始安装"
pipe = subprocess.Popen("adb shell", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
code = pipe.communicate("\n".join(cmds) + "\n");
print code
print "安装结束"