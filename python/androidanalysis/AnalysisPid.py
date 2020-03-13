# -*- coding:utf-8 -*-

import os
import threading
import traceback
from adbUtils import *
from TimeUtils import *
from logFile import *
from SoftwareUtils import *
from ObservedProcess import getObservedLists
from ObservedProcess import addProcessInfo
from ObservedProcess import isNullprocessInfo
from ObservedProcess import haveProcessInfo
from ObservedProcess import getProcessInfo
from ObservedProcess import key_process_pid
# from ObservedProcess import key_process_startTime
from ObservedProcess import key_process_stopTime
from Constant import getOver


def pidPro(env, _StopMark, interval=60):
    # global pidtimer
    threading.Thread(target=obtainpid, args=(env, _StopMark, interval)).start()
    # pidtimer = Timer(interval, pidPro, (env,))
    # pidtimer.start()


# 获取pid
def obtainpid(env, _StopMark, interval=60):
    def obtain_psinfo(content):
        return content

    while True:
        psinfo = runAdbCommand(env, ['shell', 'ps'], check=obtain_psinfo)
        killTime = obtainKillTime()
        pid_index = 0
        count = 0
        try:
            for partinfo in psinfo.split('\n'):
                if partinfo.find('PID') > 0:
                    pid_index = partinfo.split().index('PID')
                for process in getObservedLists():
                    processsearchinfo = re.compile('%s$' % process).search(partinfo.strip())
                    t = time.strftime('%Y-%m-%d_%H%M%S', time.localtime())
                    if processsearchinfo:
                        txz_pid = partinfo.split()[pid_index]
                        writeLog(env, '>>>当前%s的PID为：%s' % (process, txz_pid))
                        # fd
                        obtainfd(env, t, txz_pid, process)
                        # task
                        obtaintask(env, t, txz_pid, process)
                        # 不允许出现多个进程 ， 需要进行 打印
                        if isNullprocessInfo(process, key_process_pid):
                            addProcessInfo(process, key_process_pid, txz_pid)
                        elif not haveProcessInfo(process, key_process_pid, txz_pid):  # 不存在
                            writeLog(env,
                                     '>>>{0}被杀，历史pid为：{1}'.format(process,
                                                                  str(getProcessInfo(process, key_process_pid))))
                            addProcessInfo(process, key_process_stopTime, killTime)
                            addProcessInfo(process, key_process_pid, txz_pid)
                            threading.Thread(target=getReport, args=(env, 'txz_killed', False)).start()
                        else:
                            pass
                            # addProcessInfo(process, key_process_pid, txz_pid)
                        count += 1
                if count >= 2:
                    break
            else:
                writeLog(env, '>>>当前系统 获取指定 进程 的PID获取失败(进程名为：' + str(getObservedLists()) + ")")
        except:
            writeLog(env, 'error:{0}\n{1}'.format(traceback.print_exc(), str([psinfo])))
        if _StopMark.value:
            break
        time.sleep(interval)
    writeLog(env, "fd 和 task 获取完成")
    # if len(svr0pidlist) >1:
    #     writeLog(env,'>>>svr0被杀过，pid为：'+str(svr0pidlist))
