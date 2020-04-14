# -*- coding:utf-8 -*-

from SceneUtils import *
from TimerUtils import *
from androidanalysis.analysis.AnalysisCPU import *
from androidanalysis.analysis.AnalysisMem import *
from androidanalysis.analysis.AnalysisDataTraffic import *
from SoftwareUtils import *
from androidanalysis.constant.ObservedProcess import getObservedLists
from androidanalysis.constant.ObservedProcess import getprocessInfoKeyLen
from androidanalysis.constant.ObservedProcess import key_process_pid
from burnningUtils import stopPreburn
from androidanalysis.constant.ObservedProcess import setObservedLists

from androidanalysis.constant.Process_Constant import get_info, set_info
from envUtils import genEnv
from PCMUtils import obtainPcmList
from FileUtils import closeProc

def child_process(_StopMark, recv_conn):
    """ 一直在读管道的数据 """
    while True:
        info = recv_conn.recv()
        set_info(info)
        beginTest(info, _StopMark)
    pass


def init_env(_StopMark):
    info = get_info()
    setObservedLists(info.process_names)  # 取出 被观察的 包名
    env = genEnv(info.dev)
    writeLog(env, "开启所有日志开关")
    openlog(env)  # 开启所有的日志
    writeLog(env, "强杀 Core 的进程：com.txznet.txz")
    killApkPid(env, 'com.txznet.txz')
    writeLog(env, "删除设备原有的 crash pcm asr 的数据")
    deleteOldCrashfile(env)
    writeLog(env, "取出当前设备的Core 的apk")
    # pullInitialAPK(env)  # 取出 core 的apk  #FIXME: 耗时太久
    if info.mode != 3:
        writeLog(env, "您选择了 模式" + str(info.mode))
        writeLog(env, "开始为您取出本目录所有的pcm文件夹")
        fileList = obtainPcmList()
        if len(fileList) == 0:
            writeLog("请更改当前的模式 或者 导入您需要 老化的音频数据到 pcm文件夹")
            return None
        print ("size : " + str(fileList[0]))
        # writeLog(env, "正在为您将 " + str(fileList[0]) + " 中的数据 导入到设备")
        ret = prepareDevice(env, _StopMark, fileList[0])
        if ret == -1:
            writeLog(env, "请确定 老化工具的apk 在当前目录上面")
            return None
        if ret == -2:
            writeLog(env, "已被中断执行")
            return None
        # 如果 打开切换音频集 的开关选项， 则需要每隔一定的时间进行音频集的切换
        if info.is_open_change_pcm_list():
            print("该功能未实现，被我删掉了。")
            scene_list = [fileList[0]]
            changeSceneTimer(env, fileList, scene_list, info.mode, info.wifi_change_interval, 1,
                             info.is_open_change_pcm_list_interval())
    writeLog(env, "开始在设备中创建文件夹")
    runAdbCommand(env, ['shell', 'mkdir', '-p', '/sdcard/hprof'])
    runAdbCommand(env, ['pull', '/proc/net/xt_qtaguid/stats', os.path.join(env['flow'], 'stats_' + str(time.time()))])
    writeLog(env, "开始为您拉取 hprof 文件")
    start_hprof(env)
    writeLog(env, "正在为您发送广播")
    startPreburn(env, info.mode, info.wifi_change_interval)

    return env


# 开始测试
def beginTest(info, _StopMark):
    # removeStateFile(stopApkMark)  # 删除 文件
    # removeStateFile(successMark)
    # setObservedLists(processlist)  # 取出 被观察的 包名
    # env = genEnv(dev)
    # openlog(env)  # 开启所有的日志
    # killApkPid(env, 'com.txznet.txz')
    env = init_env(_StopMark)
    startTime = obtainTime()
    writeLog(env, "开始抓取数据 cpu mem pid 的数据")
    while True:
        excute(env, _StopMark, info.mode)
        if _StopMark.value:
            mytimercancel(env, True)
            break
        checkConnect(env, False)
    writeLog(env, "开始为您分析数据")
    try:
        global sceneTimer
        sceneTimer.cancel()
    except:
        pass
    endTime = obtainTime()
    stopPreburn(env, info.mode)
    runAdbCommand(env, ['pull', '/proc/net/xt_qtaguid/stats', os.path.join(env['flow'], 'stats_' + str(time.time()))])
    # writeLog(env,
    #          '-------------------------------------------Test Over-------------------------------------------\ntest scene:{0}'.format(
    #              ','.join(s.decode('gbk').encode('utf-8') for s in sceneList)))
    writeLog(env, "获取日志信息【1个小时抓取一次】")
    getReport(env, 'TestOver', Timeing=False)
    writeLog(env, "获取当前的hprof")
    obtainHprof(env, 'end')
    time.sleep(3)

    writeLog(env, "拉取文件 asr hprof 文件到电脑上")
    runAdbCommand(env, ['pull', '/sdcard/preburning/asr', env['result']])
    runAdbCommand(env, ['pull', '/sdcard/hprof/', env['hprof']])
    writeLog(env,
             '-------------------------------------------开始数据统计-------------------------------------------------------------')
    mHouer = consumeHour(consumeTime(startTime, endTime))
    writeLog(env, '始于：{0}，终于：{1}，总试耗时：{2:.2f}H'.format(str(startTime), str(endTime), mHouer))
    flowCounter(env, obtainuserid(env), mHouer)

    for process in getObservedLists():
        killed_count = getprocessInfoKeyLen(process, key_process_pid)
        if killed_count == 0:
            writeLog(env, '进程：{0}，未启动过;'.format(process))
        else:
            writeLog(env, '进程：{0}，被杀{1}次;'.format(process, killed_count - 1))

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
