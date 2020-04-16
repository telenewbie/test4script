# -*- coding:utf-8 -*-
import os
import re

# import psutil

# 同听/微信统计开关，默认False关闭
MusicWebchatSwitch = False

# core版本，默认为2即为合并版本，如果其他版本，请修改本值！！！一个进程的版本设置为1，三个进程的版本设置为3
coreversion = 2

# 邮箱服务器
host = 'smtp.163.com'
port = '25'

# 路径
_ENV_PCM = '/sdcard/preburning/'
_TXZ_path = '/sdcard/txz/'
corelib_dev_path = r'/system/app/TXZCore/lib/'
core_dev_path = r'/system/app/TXZCore/'
system_app_path = r'/system/app/'

Core = 'com.txznet.txz'
Preburning = 'com.txznet.preburning'

successMark = os.path.join(os.getcwd(), 'isFinish')
stopApkMark = os.path.join(os.getcwd(), 'isStopApk')

errorstauts = False

#######################程序是否结束
# isOver = False
from multiprocessing import Value

isOver = Value('b', False)


def setOver(over):
    global isOver
    isOver.value = over


def getOver():
    global isOver
    return isOver.value


# -------------- 索引
cpu_info = -1
memoryinfo_rss = -1
nameinfo = -1

# -----------------------------------------------------------------------------
# 正则规则
__RE_REMOTE_DEV = re.compile(r'^\d+\.\d+\.\d+\.\d+(:\d+)?$')  # 匹配IP地址的设备
__RE_IP_ADRESS = re.compile(r'^\d+\.\d+\.\d+\.\d+(:\d+)?')
__RE_APK_PATH = re.compile('(?::).+')
_RE_SYSLOGTIME = re.compile(r'\d+_\d+')
_RE_TTSAPK = re.compile('start loadRes path:(.+?.apk)')

# ------------------默认值
DEFAULT_INTERVAL_CPU = 5
DEFAULT_INTERVAL_MEM = 10
DEFAULT_INTERVAL_PULL_LOG = 3600
DEFAULT_INTERVAL_PID = 10
DEFAULT_INTERVAL_CHANGE_WIFI = 0
DEFAULT_INTERVAL_CHANGE_PCM = 7200
DEFAULT_INTERVAL_CHANGE_PCM_CONTINUE = 300
DEFAULT_INTERVAL_SAVE_DATA = 600

# ---------------------------文件有效大小
VERIFY_MEM_FILE_SIZE = 2048
