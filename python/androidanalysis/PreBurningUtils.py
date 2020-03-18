# -*- coding:utf-8 -*-

import os
import time
import base64
import threading
from FileUtils import *
from Constant import *
from envUtils import *
from logFile import writeLog
from logFile import openlog
from TimeUtils import *
from PCMUtils import *
from adbUtils import *
from SceneUtils import *
from TimerUtils import *
from AnalysisCPU import *
from AnalysisMem import *
from AnalysisDataTraffic import *
from SoftwareUtils import *
from ObservedProcess import getProcessInfo
from ObservedProcess import getObservedLists
from ObservedProcess import getprocessInfoKeyLen
from ObservedProcess import key_process_pid
from burnningUtils import stopPreburn
from ObservedProcess import setObservedLists


# 开始测试
def beginTest(_StopMark, processlist, _TimeValue, _switchMode, _intervalVar, testModel, dev=None):
    removeStateFile(stopApkMark)
    removeStateFile(successMark)
    setObservedLists(processlist)
    env = genEnv(dev)
    openlog(env)  # 开启所有的日志
    killApkPid(env, 'com.txznet.txz')
    startTime = obtainTime()
    deleteOldCrashfile(env)
    fileList = obtainPcmList()
    pullInitialAPK(env)  # 取出 core 的apk
    sceneList = []
    if testModel != 3:
        if fileList.count == 0:
            writeLog("请导入 语音pcm文件")
            return False
        sceneList.append(fileList[0])
        if not prepareDevice(env, _StopMark, fileList[0]):
            closeProc(successMark)
            print '-------------------------------------------Test Over-------------------------------------------'
            return False
        if testModel == 1 and _switchMode:
            changeSceneTimer(env, fileList, sceneList, testModel, _TimeValue, 1, _intervalVar)
    runAdbCommand(env, ['shell', 'mkdir', '-p', '/sdcard/hprof'])
    runAdbCommand(env, ['pull', '/proc/net/xt_qtaguid/stats', os.path.join(env['flow'], 'stats_' + str(time.time()))])
    if _StopMark.value:
        closeProc(successMark)
        return False
    obtainHprof(env, 'start')
    Timer(60 * 10, obtainHprof, (env, 'start10m',)).start()
    startPreburn(env, testModel, _TimeValue)
    writeLog({}, "newbie start execute")
    while True:
        excute(env, _StopMark, testModel)
        if _StopMark.value:
            mytimercancel(env, True)
            break
        checkConnect(env, False)
    global sceneTimer
    writeLog({}, "newbie start analysis")
    try:
        sceneTimer.cancel()
    except:
        pass
    endTime = obtainTime()
    stopPreburn(env, testModel)
    runAdbCommand(env, ['pull', '/proc/net/xt_qtaguid/stats', os.path.join(env['flow'], 'stats_' + str(time.time()))])
    writeLog(env,
             '-------------------------------------------Test Over-------------------------------------------\ntest scene:{0}'.format(
                 ','.join(s.decode('gbk').encode('utf-8') for s in sceneList)))
    getReport(env, 'TestOver', Timeing=False)
    obtainHprof(env, 'end')
    time.sleep(3)
    runAdbCommand(env, ['pull', '/sdcard/preburning/asr', env['result']])
    runAdbCommand(env, ['pull', '/sdcard/hprof/', env['hprof']])
    writeLog(env,
             '-------------------------------------------开始数据统计-------------------------------------------------------------')
    mHouer = consumeHour(consumeTime(startTime, endTime))
    writeLog(env, '始于：{0}，终于：{1}，总试耗时：{2:.2f}H'.format(str(startTime), str(endTime), mHouer))
    flowCounter(env, obtainuserid(env), mHouer)
    for process in getObservedLists():
        writeLog(env, '进程：{0}，被杀{1}次;'.format(process, getprocessInfoKeyLen(process, key_process_pid)))
        pass
    writeLog(env, '--------------------内存数据-----------------------')
    memTrend(env)
    # 通过dumpsys meminfo 的数据都画在一张图上
    exc_memdata(env)
    # 分别绘制各自的内存数据 都 各自的图上
    memoryAnalysis(env)
    writeLog(env, '--------------------CPU数据-----------------------')
    commonanalysedata(env)
    obtianCrashCount(env)
    writeLog(env,
             '-------------------------------------------统计结束-------------------------------------------------------------')
    closeProc(successMark)
    # print threading.active_count()
    pl.show(block=True)  # 所有图关闭，退出阻塞
