#coding:utf-8
import subprocess

p = subprocess.Popen(['adb', 'devices'], stdout=subprocess.PIPE)
outstr, errstr = p.communicate()
print str(outstr)+r"""\t"""
import os
fff=os.system("adb devices")
print str(fff)+r"""\t"""
pipe=os.popen("adb devices")
print pipe.readlines()



#读取设备列表
def readDeviceList():
    #先执行一遍adb devices
    os.system('adb devices')
    ret = []
    p = subprocess.Popen(['adb', 'devices'], stdout=subprocess.PIPE)
    outstr, errstr = p.communicate()
    for dev in outstr.splitlines()[1:]:
        ret.append(dev.split("\t")[0])
    return ret
print readDeviceList()