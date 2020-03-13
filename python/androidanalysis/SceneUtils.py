# -*- coding:utf-8 -*-

import os
import time
import datetime
import re
from threading import Timer
import threading
from adbUtils import *
from Constant import _ENV_PCM
from logFile import *
from hprofUtils import *
from PreBurningUtils import *
from burnningUtils import stopPreburn


def changeSceneTimer(env, filelist, scenelist, testModel, _TimeValue, index, intervalVar):
    global sceneTimer
    sceneTimer = Timer(7200, scenePro, (env, filelist, scenelist, testModel, _TimeValue, index, intervalVar))
    sceneTimer.start()


def scenePro(env, filelist, scenelist, testModel, _TimeValue, index, intervalVar):
    global sceneTimer
    threading.Thread(target=changeScene,
                     args=(env, filelist, scenelist, testModel, _TimeValue, index, intervalVar)).start()
    index += 1
    if index == len(filelist):
        index = 0
    sceneTimer = Timer(7200, scenePro, (env, filelist, scenelist, testModel, _TimeValue, index, intervalVar))
    sceneTimer.start()


def changeScene(env, filelist, scenelist, testModel, _TimeValue, index, intervalVar):
    stopPreburn(env, testModel)
    orgPath = filelist[index]
    scenelist.append(orgPath)
    runAdbCommand(env, ['shell', 'rm', '/sdcard/preburning/pcm/*'])
    pushfiletoandroid(env, orgPath, _ENV_PCM + 'pcm/')
    writeLog(env, 'Current Scene:{0}'.format(orgPath))
    if intervalVar:
        time.sleep(60 * 5)
    obtainHprof(env, filelist[index - 1])
    startPreburn(env, testModel, _TimeValue)
