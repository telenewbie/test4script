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


def pidPro(env, _StopMark, interval=5):
    # global pidtimer
    threading.Thread(target=obtainpid, args=(env, _StopMark, interval)).start()

    # pidtimer = Timer(interval, pidPro, (env,))
    # pidtimer.start()


def obtain_psinfo(content):
    return content


def checkEmpty(value):
    return value == "" or value is None


def getPidFromPackage(env, process):
    psinfo = runAdbCommand(env, ['-s', env['dev'], 'shell', 'ps -ef |grep ', process, "|grep -v grep"],
                           check=obtain_psinfo)
    # print "ps -ef|grep ", process, ",result=", tuple(psinfo), psinfo == ""
    if checkEmpty(psinfo):
        psinfo = runAdbCommand(env, ['-s', env['dev'], 'shell', 'ps |grep ', process, "|grep -v grep"],
                               check=obtain_psinfo)
        # print "ps |grep ", process, ",result=", psinfo
        if checkEmpty(psinfo):
            return -1
    if len(str(psinfo)) <= 0:
        return -1

    # 找到哪一行
    psinfo = psinfo.split("\n")
    # print psinfo

    for ps in psinfo:
        # print ps
        ps = ps.split(" ")
        ps = [x for x in ps if len(x.strip())]
        # print ("hello " + ps[-1].strip())
        print ps[-1].strip()
        if ps[-1].strip() == process:
            print("i find it " + ps[0] + ":" + ps[1])
            return int(ps[1])
    # print "sth occur error "
    return -1


def checkValue(value):
    '''
    测试是否 行数达到 10条，没有则认为不合法的数据
    :param value:
    :return:
    '''
    return len(value.split('\n')) > 10


# 获取pid
def obtainpid(env, _StopMark, interval):
    while True:
        psinfo = runAdbCommand(env, ['shell', 'ps'], check=obtain_psinfo)
        # 判断psinfo的有效性
        if not checkValue(psinfo):
            psinfo = runAdbCommand(env, ['shell', 'ps -ef'], check=obtain_psinfo)
            pass
        killTime = obtainKillTime()
        pid_index = 0
        count = 0

        try:
            # 进程号发生变更才会被检测到，如果 进程号 死掉，未起来 则不会打印
            for partinfo in psinfo.split('\n'):
                # print partinfo
                if partinfo.find('PID') > 0:
                    pid_index = partinfo.split().index('PID')
                for process in getObservedLists():
                    # print process in psinfo, "????"
                    processsearchinfo = re.compile('%s$' % process).search(partinfo.strip())
                    t = time.strftime('%Y-%m-%d_%H%M%S', time.localtime())
                    # print ">>>>", process, "<<<<", processsearchinfo
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
            # else:
            #     writeLog(env, '>>>当前系统 获取指定 进程 的PID获取失败(进程名为：' + str(getObservedLists()) + ")" + str([psinfo]))
        except:
            writeLog(env, 'error:{0}\n{1}'.format(traceback.print_exc(), str([psinfo])))
        if _StopMark.value:
            break
        time.sleep(interval)
    writeLog(env, "fd 和 task 获取完成")
    # if len(svr0pidlist) >1:
    #     writeLog(env,'>>>svr0被杀过，pid为：'+str(svr0pidlist))
