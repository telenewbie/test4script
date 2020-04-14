# -*- coding:utf-8 -*-

from androidanalysis.analysis.AnalysisPid import *
from androidanalysis.analysis.AnalysisMem import *


# 定时拉取日志 crash anr tombstones 等 到指定的文件夹
def getReport(env, action='', interval=3600, Timeing=True):
    global txzlogtimer
    root = env.get('dir', None)
    log_path = os.path.join(root, action + time.strftime('%Y%m%d_%H%M%S'))
    os.makedirs(log_path)
    threading.Thread(target=pullLog, args=(env, log_path)).start()
    if Timeing:
        # 6 * 60 * 10 s= 1h 一个小时之后的定时器
        txzlogtimer = Timer(interval, getReport, (env, 'txzlog_'))
        # txzlogtimer = Timer(1320,getReport,(env,))
        txzlogtimer.start()
    print 'obtain log compeled'


# 内存PID定时器集合
def mytimer(env, _StopMark):
    global txzlogtimer
    global pidtimer
    global memtimer
    from Process_Constant import get_info
    info = get_info()
    txzlogtimer = Timer(info.interval_pull_log, getReport, (env, 'txzlog_', info.interval_pull_log))
    pidtimer = Timer(info.interval_pid_fd_task, pidPro, (
        env, _StopMark, info.interval_pid_fd_task
    ))
    memtimer = Timer(info.interval_mem, memPro, (env, _StopMark, info.interval_mem))
    memtimer.start()
    pidtimer.start()
    txzlogtimer.start()


# 取消所有定时器
def mytimercancel(env, timerMark):
    try:
        while timerMark:
            for i in threading.enumerate():
                if type(i) == threading._Timer:
                    i.cancel()
            time.sleep(0.1)
            for i in threading.enumerate():
                if type(i) == threading._Timer:
                    timerMark = True
                    break
                else:
                    timerMark = False
    except:
        writeLog(env, traceback.print_exc())
    return timerMark
