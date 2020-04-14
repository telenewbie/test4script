# -*- coding:utf-8 -*-

from androidanalysis.config.Constant import _ENV_PCM
from PreBurningUtils import *
from burnningUtils import stopPreburn
from androidanalysis.Process_Constant import get_info


def changeSceneTimer(env, filelist, scenelist, testModel, _TimeValue, index, intervalVar):
    global sceneTimer
    info = get_info()
    sceneTimer = Timer(info.change_pcm_list_interval, scenePro,
                       (env, filelist, scenelist, testModel, _TimeValue, index, intervalVar))
    sceneTimer.start()


def scenePro(env, filelist, scenelist, testModel, _TimeValue, index, intervalVar):
    global sceneTimer
    threading.Thread(target=changeScene,
                     args=(env, filelist, scenelist, testModel, _TimeValue, index, intervalVar)).start()
    index += 1
    if index == len(filelist):
        index = 0
    info = get_info()
    sceneTimer = Timer(info.change_pcm_list_interval, scenePro, (env, filelist, scenelist, testModel, _TimeValue, index, intervalVar))
    sceneTimer.start()


def changeScene(env, filelist, scenelist, testModel, _TimeValue, index, intervalVar):
    stopPreburn(env, testModel)
    orgPath = filelist[index]
    scenelist.append(orgPath)
    runAdbCommand(env, ['shell', 'rm', '/sdcard/preburning/pcm/*'])
    pushfiletoandroid(env, orgPath, _ENV_PCM + 'pcm/')
    writeLog(env, 'Current Scene:{0}'.format(orgPath))
    if intervalVar:
        info = get_info()
        time.sleep(info.change_pcm_interval)
    obtainHprof(env, filelist[index - 1])
    startPreburn(env, testModel, _TimeValue)
