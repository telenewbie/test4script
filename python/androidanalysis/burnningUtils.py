# -*- coding:utf-8 -*-
from logFile import writeLog
from adbUtils import runAdbCommand


# 停止老化
def stopPreburn(env, testModel):
    if testModel == 1:
        runAdbCommand(env, ['shell', 'am', 'broadcast', '-a', 'com.txznet.preburning.stop'])
        writeLog(env, 'excute:' + ' '.join(['shell', 'am', 'broadcast', '-a', 'com.txznet.preburning.stop']))
    elif testModel == 2:  # 文本模式
        runAdbCommand(env, ['shell', 'am', 'broadcast', '-a', 'com.txznet.preburning.stop', '--ei', 'model', '2'])
        writeLog(env, 'excute:' + ' '.join(
            ['shell', 'am', 'broadcast', '-a', 'com.txznet.preburning.stop', '--ei', 'model', '2']))
    elif testModel == 3:  # 什么都不做
        pass
