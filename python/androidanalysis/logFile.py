# -*- coding:utf-8 -*-

import sys
import time
# from adbUtils import *
from Constant import _TXZ_path
from Constant import _RE_SYSLOGTIME
import tkMessageBox
import os


# 日志接口
def writeLog(env, msg):
    dev = env.get('dev', None)
    log = env.get('log', None)
    t = time.time()
    tm = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t)) + ('.%03d' % (round(t * 1000) % 1000))
    msg = '[%s][%s]%s\n' % (tm, dev, msg)
    try:
        sys.stdout.write(msg.decode('utf-8').encode('gbk'))
    except:
        sys.stdout.write(msg)
    if log is not None:
        log.write(msg)
        log.flush()  # 将缓存中所有内容清空写入文件


# 日志接口
def checklog(env, checkString):
    currentTime = time.time()
    print "checklog: ", env['syslogpath'], "<<>>", os.listdir(env['syslogpath'])
    print sorted(os.listdir(env['syslogpath']), reverse=True)
    for filename in sorted(os.listdir(env['syslogpath']), reverse=True):
        filetime = _RE_SYSLOGTIME.search(filename).group()
        if filetime:
            filetimestamp = time.mktime(time.strptime(filetime, '%Y%m%d_%H%M%S'))
            value = currentTime - filetimestamp
            if 0 <= value and value <= 900:  # 15min内
                with open(os.path.join(env['syslogpath'], filename)) as filedata:
                    for line in filedata:
                        if line.find(checkString) >= 0:
                            writeLog(env, '>>>{0}:{1}'.format(filename, line.strip()))
                            return line.strip()
    return False


# 本地打印
def localprint(str):
    print str.decode('utf-8').encode("GBK")


# 错误提示，弹窗并打印
def error_tip(str):
    localprint(str)
    tkMessageBox.showinfo('ERROR', str)
