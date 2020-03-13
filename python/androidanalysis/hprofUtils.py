# -*- coding:utf-8 -*-

import os
import time
import datetime
import re
from adbUtils import *
from ObservedProcess import getObservedLists


# 生成hprof
def obtainHprof(env, scene=''):
    for process in getObservedLists():
        file1 = '/sdcard/hprof/{0}_{1}_scene.hprof'.format(process, time.strftime('%Y%m%d_%H%M%S'))
        runAdbCommand(env, ['shell', 'am', 'dumpheap', process, file1])
        if scene != '':
            runAdbCommand(env, ['shell', 'mv', file1, file1.replace('scene', scene)])


def obtainMusicHprof(env):
    file1 = '/sdcard/hprof/music_{0}.hprof'.format(time.strftime('%Y%m%d_%H%M%S'))
    runAdbCommand(env, ['shell', 'am', 'dumpheap', 'com.txznet.music', file1])
