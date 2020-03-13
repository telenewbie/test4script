# -*- coding:utf-8 -*-

import os
import time
import datetime
import re
import pylab as pl
from logFile import *
from ProcessUtils import get_process

# ----------------------------------meminfo-图表生成----------------------------------------------------
line = ['b', 'g', 'r', 'c', 'm', 'y', 'k']


def mem_draw(env, process_name, dict, adress, xlist, unit='MB'):
    title = ''
    # 如果进程名称包含: 则需要进行 替换， 否则文件写入失败,
    #
    # process_name = process_name.replace(":", "_")

    picture = pl.figure('{0}------Memory'.format(process_name), figsize=[23, 12])
    count = 0
    for item, mList in dict.items():
        maxvalue = max(mList)
        meanvalue = mean(mList)
        # print "maxvalue:" + str(maxvalue)
        # print "minvalue:" + str(meanvalue)
        # print "count:" + str(count)
        # print "title:" + title
        # print "line[count]:" + line[count]
        # print "item:" + item
        # print "xlist:" + str(xlist)
        # print "ylist:" + str(mList)
        if title:
            if count % 3 == 0 and count != 0:
                title += '\n'
            else:
                title += ' | '
        title += '{0}_mean={1:.2f}{3},{0}_max={2:.2f}{3}'.format(item, meanvalue, maxvalue, unit)
        # format_string 由颜色字符，风格字符，和标记字符
        pl.plot(xlist, mList, 'o{0}-'.format(line[count]), label=item)  # error 就是要用差值

        count += 1
        if count >= 7:
            count = 0
    title = 'Time Consuming:  ' + str(timeformat(adress)) + '\n' + title
    # writeLog(env,'{1} Memory: {0}'.format(title.replace('\n',' | '),process_name.upper()))
    pl.title(title)
    pl.legend(loc='best')
    pl.xlabel('Time(s)')
    pl.ylabel('Size({0})'.format(unit))
    imgpath = os.path.join(env['result'], '{0}------Memory.png'.format(get_process(process_name)))
    picture.savefig(imgpath)
    pl.show(block=False)


def mean(list):
    sum = 0
    for item in list:
        sum += item
    mean = sum / len(list)
    return mean


time_pattern = re.compile('\d+-\d+-\d+_\d+')


def timeformat(adress):
    list = os.listdir(adress)
    startTime = time_pattern.search(list[0]).group()
    stopTime = time_pattern.search(list[-1]).group()
    return datetime.datetime.strptime(stopTime, "%Y-%m-%d_%H%M%S") - datetime.datetime.strptime(startTime,
                                                                                                "%Y-%m-%d_%H%M%S")


# CPU画图
def cpu_draw(env, name, dict, Optional=False):
    Percentage = '%'
    title = ''
    picture = pl.figure('{0}------CPU'.format(name), figsize=[23, 12])
    count = 0
    # print dict
    for item, values in dict.items():
        meanvalue = common_mean(values)
        maxvalue = max(values)
        if title:
            if count % 3 == 0 and count != 0:
                title += '\n'
            else:
                title += ' | '
        title += '{0}_mean={1}{3},{0}_max={2}{3}'.format(item, meanvalue, maxvalue, Percentage)
        pl.plot(range(0, len(values)), list(values), 'o{0}-'.format(line[count]), label=item)
        count += 1
        if count >= 7:
            count = 0
    writeLog(env, 'CPU: {0}'.format(title.replace('\n', ' | ')))
    pl.title(title)
    pl.legend(loc='best')
    pl.xlabel('Time(s)')
    pl.ylabel('Percentage(%)')
    imgpath = os.path.join(env['result'], '{0}------CPU.png'.format(name))
    picture.savefig(imgpath)
    pl.show(block=False)
    # img = Image.open(imgpath)
    # img.show()


# 求均值
def common_mean(list):
    sum = 0.0
    for temp in list:
        sum += temp
    return round(sum / len(list), 2)
