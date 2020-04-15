# -*- coding:utf-8 -*-

import datetime
import re
import time

time_pattern = re.compile('\d+-\d+-\d+_\d+')


def timeformat(adress):
    from osUtils import listdir
    list = listdir(adress)
    startTime = time_pattern.search(list[0]).group()
    stopTime = time_pattern.search(list[-1]).group()
    return datetime.datetime.strptime(stopTime, "%Y-%m-%d_%H%M%S") - datetime.datetime.strptime(startTime,
                                                                                                "%Y-%m-%d_%H%M%S")


# 获取当前时间，精度到毫秒
def obtainTime():
    t = time.time()
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t)) + ('.%03d' % (round(t * 1000) % 1000))
    return currentTime


# 获取当前时间，精度到秒
def obtainKillTime():
    currentTime = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
    return currentTime


# 计算耗时，未启用？
def consumeTime(start_time, end_time):
    start_timelist = start_time.split('.')
    end_timelist = end_time.split('.')
    return datetime.datetime.strptime(end_timelist[0], "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
        start_timelist[0], "%Y-%m-%d %H:%M:%S")


# 计算耗时，以日志文件中的时间统计
def testTime(startFile, endFile):
    startTime = time_pattern.search(startFile).group()
    stopTime = time_pattern.search(endFile).group()
    return datetime.datetime.strptime(stopTime, "%Y-%m-%d_%H%M%S") - datetime.datetime.strptime(startTime,
                                                                                                "%Y-%m-%d_%H%M%S")


def consumeMin(currentTime):
    total_seconds = currentTime.total_seconds()
    return total_seconds / 60


def consumeHour(currentTime):
    total_seconds = currentTime.total_seconds()
    return total_seconds / 3600


def consumeS(currentTime):
    return currentTime.total_seconds()


def rakeRatio(startValue, endValue, time):
    return (endValue - startValue) / time


def realKillTime(oriTime):
    mlist = oriTime.split('_')
    mlist[-1] = '_' + str(int(mlist[-1]) - 100)
    return ''.join(mlist)
