# -*- coding:utf-8 -*-

import traceback

from TimerUtils import *
from adbUtils import *
from SoftwareUtils import *
from ObservedProcess import getObservedLists
from ObservedProcess import key_process_cpu
from ObservedProcess import addProcessInfo
from PreBurningUtils import *
from burnningUtils import stopPreburn
from hprofUtils import *
from Constant import nameinfo
from Constant import cpu_info

from Constant import errorstauts
import collections
import numpy as np
from ObservedProcess import printInfos


# 分析 CPU


# 抓取数据
# top 线程 前 50的数据
# top 进程 前 10的数据
# logcat -v time 的数据
def excute(env, _StopMark, testModel):
    global errorstauts
    global sceneTimer
    writeLog(env, '>>>开始抓取TOP数据')
    # 定时启动项
    mytimer(env,_StopMark) #FIXMe 暂时注释
    timerMark = True
    _top_thread_cmd = ['adb', '-s', env['dev'], 'shell', 'top', '-t', '-d', '1', '-m', '50']
    _top_thread_p = subprocess.Popen(_top_thread_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _syslog_cmd = ['adb', '-s', env['dev'], 'logcat', '-v', 'time']
    _syslog_p = subprocess.Popen(_syslog_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _top_process_cmd = ['adb', '-s', env['dev'], 'shell', 'top', '-d', '1', '-m', '10']
    _top_process_p = subprocess.Popen(_top_process_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    count = 51200
    while not _StopMark.value:
        if os.path.exists(stopApkMark):
            try:
                sceneTimer.cancel()
            except:
                pass
            stopPreburn(env, testModel)
            os.remove(stopApkMark)
            obtainHprof(env)
        easytime = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        syslog_file_name = 'SYS_%s.log' % (easytime)
        Top_thread_file_name = 'Top_thread_data_%s.log' % (easytime)
        Top_process_file_name = 'Top_process_data_%s.log' % (easytime)
        with open(os.path.join(env['syslogpath'], syslog_file_name), 'wb') as syslog_file, \
                open(os.path.join(env['top_thread_logpath'], Top_thread_file_name), 'wb') as top_thread_file, \
                open(os.path.join(env['top_process_logpath'], Top_process_file_name), 'wb') as top_process_file:
            while count:
                if os.path.exists(stopApkMark):
                    try:
                        sceneTimer.cancel()
                    except:
                        pass
                    stopPreburn(env, testModel)
                    os.remove(stopApkMark)
                    obtainHprof(env)
                count -= 1
                if _StopMark.value:
                    break
                else:
                    _top_thread_p, top_thread_file = writeWithPOpen(env, _top_thread_p, top_thread_file,
                                                                    env['top_thread_logpath'], Top_thread_file_name,
                                                                    _top_thread_cmd)
                    _syslog_p, syslog_file = writeWithPOpen(env, _syslog_p, syslog_file, env['syslogpath'],
                                                            syslog_file_name, _syslog_cmd)
                    _top_process_p, top_process_file = writeWithPOpen(env, _top_process_p, top_process_file,
                                                                      env['top_process_logpath'], Top_process_file_name,
                                                                      _top_process_cmd)
                syslog_file.write(_syslog_p.stdout.readline().strip() + '\n')
                top_thread_file.write(_top_thread_p.stdout.readline().strip() + '\n')
                top_process_file.write(_top_process_p.stdout.readline().strip() + '\n')
                if errorstauts:
                    _StopMark.value = True
            if _StopMark.value:
                try:
                    sceneTimer.cancel()
                except:
                    pass
                writeWithPOpen(env, _top_thread_p, top_thread_file, env['top_thread_logpath'], Top_thread_file_name,
                               _top_thread_cmd, True)
                writeWithPOpen(env, _syslog_p, syslog_file, env['syslogpath'], syslog_file_name, _syslog_cmd, True)
                writeWithPOpen(env, _top_process_p, top_process_file, env['top_process_logpath'], Top_process_file_name,
                               _top_process_cmd, True)
                timerMark = mytimercancel(env, timerMark)
                break
            syslog_file.close()
            top_thread_file.close()
            top_process_file.close()
            count = 51200
            if errorstauts:
                _StopMark.value = True


# 清理出现异常的进程
# closeObtain 更名为 writeWithPOpen
def writeWithPOpen(env, p, log_file, logpath, logfilename, cmd, killmark=False):
    if p.poll() != None or killmark:
        a = p.stdout.flush()
        if a != None:
            try:
                log_file.write(a)
            except:
                writeLog(env, traceback.print_exc())
                log_file.close()
                log_file = open(os.path.join(logpath, logfilename), 'wb')
                log_file.write(a)
        if not killmark:
            return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE), log_file
        else:
            return None, log_file
    return p, log_file


# 查找CPU/MEM
def exc_search(data, regular, cpu_list):
    global cpuinfo
    search_result = re.findall(regular, data)
    if search_result:
        cpu_list.append(float(search_result[0].strip().split()[cpuinfo].strip('%')))
        return True
    else:
        return False


# 处理日志数据
def obtianCapabilityinfo(env, file):
    global cpu_info
    global memoryinfo_rss
    global nameinfo
    cpu_info, memoryinfo_rss, nameinfo = obtainindex(file)
    # cpu_info =2
    print cpu_info
    with open(file) as datas:
        # 数据列表
        # txzsvr1_cpu_list = []
        # txzsvr2_cpu_list = []
        # txzsvr3_cpu_list = []
        # txzsvr0_cpu_list = []
        # txz_cpu_list = []
        # webchat_cpu_list = []
        # music_cpu_list = []
        # musicplayer_cpu_list = []
        # musicsvr0_cpu_list = []
        # total
        top5_list = []
        startremind = False
        top5_count = 5

        searchmark = False  # 每一次top 数据的开始
        txzmark = True
        svr0mark = True
        svr1mark = True
        svr2mark = True
        svr3mark = True
        webcahtmark = True
        musicmark = True
        playermark = True
        musicsvr0 = True

        xCount = 0
        space_line_count = 0  # 空行
        data_line = 0  # 数据行
        lines = (line.strip() for line in datas)
        for data in lines:
            # 剔除掉空行
            if not data:  # 空行
                # print "空行" + str(space_line_count)
                if data_line > 0:
                    space_line_count = 0
                    data_line = 0
                space_line_count += 1
            else:
                data_line = 1
                if space_line_count > 1:
                    continue
                # top5统计
                startremind, top5_count = statistics_top5(data, top5_list, startremind, top5_count)
                if data.find("Name") > 0:
                    # 去除 列名
                    continue

                # 将cpu的信息存放到 dict中

                # print data
                # print cpu_info
                # print "--" + data.split()[-1]
                # print "--" + data.split()[cpu_info].strip('%')

                addProcessInfo(data.split()[-1], key_process_cpu, float(data.split()[cpu_info].strip('%')))
                #
                # # 将每一次的结果数据都进行保存
                # # 剔除掉 非有效数据的行
                # # 如果是以 "User" 或者 包含 "CPU%"  则剔除 ，这种不可靠
                # # 如果 空行 和 底下一行是包含 Name的那么就是做为开始
                # if data.find("CPU%") > 0 or data.startswith("User"):
                #     continue
                # # 获取每个进程的名称
                # lineProcessName = data.split()[-1]
                # if lineProcessName in getObservedLists():
                #     # 如果再被观测的队列中
                #
                #     pass
                #
                # if data.find('+ Idle') >= 0:
                #     xCount += 1
                #     if txzmark != svr0mark:
                #         if not svr0mark:
                #             if len(txz_cpu_list) > len(txzsvr0_cpu_list):
                #                 txzsvr0_cpu_list.append(0.0)
                #         if not txzmark:
                #             if len(txz_cpu_list) < len(txzsvr0_cpu_list):
                #                 txz_cpu_list.append(0.0)
                #     if txzmark != svr1mark:
                #         if not svr1mark:
                #             if len(txz_cpu_list) > len(txzsvr1_cpu_list):
                #                 txzsvr1_cpu_list.append(0.0)
                #         if not txzmark:
                #             if len(txz_cpu_list) < len(txzsvr1_cpu_list):
                #                 txz_cpu_list.append(0.0)
                #     if svr0mark != svr1mark:
                #         if not svr1mark:
                #             if len(txzsvr1_cpu_list) < len(txzsvr0_cpu_list):
                #                 txzsvr1_cpu_list.append(0.0)
                #         if not txzmark:
                #             if len(txzsvr1_cpu_list) > len(txzsvr0_cpu_list):
                #                 txzsvr0_cpu_list.append(0.0)
                #     if not svr2mark:
                #         if len(txz_cpu_list) > len(txzsvr2_cpu_list):
                #             txzsvr2_cpu_list.append(0.0)
                #     if not svr3mark:
                #         if len(txz_cpu_list) > len(txzsvr3_cpu_list):
                #             txzsvr3_cpu_list.append(0.0)
                #     if txzmark == False and svr0mark == False and svr1mark == False and svr2mark == False and svr3mark == False:
                #         txz_cpu_list.append(0.0)
                #         txzsvr0_cpu_list.append(0.0)
                #         txzsvr1_cpu_list.append(0.0)
                #         txzsvr2_cpu_list.append(0.0)
                #         txzsvr3_cpu_list.append(0.0)
                #     if MusicWebchatSwitch:
                #         if musicsvr0 != musicmark:
                #             if not musicmark:
                #                 if len(musicsvr0_cpu_list) > len(music_cpu_list):
                #                     music_cpu_list.append(0.0)
                #             if not musicsvr0:
                #                 if len(musicsvr0_cpu_list) < len(music_cpu_list):
                #                     musicsvr0_cpu_list.append(0.0)
                #         if playermark != musicmark:
                #             if not musicmark:
                #                 if len(musicplayer_cpu_list) > len(music_cpu_list):
                #                     music_cpu_list.append(0.0)
                #             if not playermark:
                #                 if len(musicplayer_cpu_list) < len(music_cpu_list):
                #                     musicplayer_cpu_list.append(0.0)
                #         if playermark != musicsvr0:
                #             if not musicsvr0:
                #                 if len(musicplayer_cpu_list) > len(musicsvr0_cpu_list):
                #                     musicsvr0_cpu_list.append(0.0)
                #             if not playermark:
                #                 if len(musicplayer_cpu_list) < len(musicsvr0_cpu_list):
                #                     musicplayer_cpu_list.append(0.0)
                #         if musicmark == False and musicsvr0 == False and playermark == False:
                #             music_cpu_list.append(0.0)
                #             musicsvr0_cpu_list.append(0.0)
                #             musicplayer_cpu_list.append(0.0)
                #         if not webcahtmark:
                #             webchat_cpu_list.append(0.0)
                #     searchmark = True
                #     txzmark = False
                #     svr0mark = False
                #     svr1mark = False
                #     svr2mark = False
                #     svr3mark = False
                #     webcahtmark = False
                #     musicmark = False
                #     playermark = False
                #     musicsvr0 = False
                # elif (not MusicWebchatSwitch) and (txzmark and svr1mark):
                #     continue
                # elif (MusicWebchatSwitch and txzmark and svr1mark and webcahtmark and musicmark and musicsvr0):
                #     continue
                # if searchmark:
                #     # core
                #     if not txzmark:
                #         txzmark = exc_search(data, '(.*)com.txznet.txz$', txz_cpu_list)
                #     if not svr0mark:
                #         svr0mark = exc_search(data, '(.*)com.txznet.txz:svr0$', txzsvr0_cpu_list)
                #     if not svr1mark:
                #         svr1mark = exc_search(data, '(.*)com.txznet.txz:svr1$', txzsvr1_cpu_list)
                #     if not svr2mark:
                #         svr2mark = exc_search(data, '(.*)com.txznet.txz:svr2$', txzsvr2_cpu_list)
                #     if not svr3mark:
                #         svr3mark = exc_search(data, '(.*)com.txznet.txz:svr3$', txzsvr3_cpu_list)
                #     if MusicWebchatSwitch:
                #         # webchat
                #         if not webcahtmark:
                #             webcahtmark = exc_search(data, '(.*)com.txznet.webchat$', webchat_cpu_list)
                #         # txz——同听
                #         if not musicmark:
                #             musicmark = exc_search(data, '(.*)com.txznet.music$', music_cpu_list)
                #         if not playermark:
                #             playermark = exc_search(data, '(.*)com.txznet.music:player$', musicplayer_cpu_list)
                #         if not musicsvr0:
                #             musicsvr0 = exc_search(data, '(.*)com.txznet.music:svr0$', musicsvr0_cpu_list)
        writeLog(env, 'CPU占用TOP5榜单:{0}'.format(
            str(collections.Counter(top5_list)).replace('Counter({', '').replace('}', '').replace(': ', ':(').replace(
                ',', '),')))

        # if txzmark != svr0mark:
        #     if not svr0mark:
        #         if len(txz_cpu_list) > len(txzsvr0_cpu_list):
        #             txzsvr0_cpu_list.append(0.0)
        #     if not txzmark:
        #         if len(txz_cpu_list) < len(txzsvr0_cpu_list):
        #             txz_cpu_list.append(0.0)
        # if txzmark != svr1mark:
        #     if not svr1mark:
        #         if len(txz_cpu_list) > len(txzsvr1_cpu_list):
        #             txzsvr1_cpu_list.append(0.0)
        #     if not txzmark:
        #         if len(txz_cpu_list) < len(txzsvr1_cpu_list):
        #             txz_cpu_list.append(0.0)
        # if svr0mark != svr1mark:
        #     if not svr1mark:
        #         if len(txzsvr1_cpu_list) < len(txzsvr0_cpu_list):
        #             txzsvr1_cpu_list.append(0.0)
        #     if not txzmark:
        #         if len(txzsvr1_cpu_list) > len(txzsvr0_cpu_list):
        #             txzsvr0_cpu_list.append(0.0)
        # if not svr2mark:
        #     if len(txz_cpu_list) > len(txzsvr2_cpu_list):
        #         txzsvr2_cpu_list.append(0.0)
        # if not svr3mark:
        #     if len(txz_cpu_list) > len(txzsvr3_cpu_list):
        #         txzsvr3_cpu_list.append(0.0)
        # if txzmark == False and svr0mark == False and svr1mark == False and svr2mark == False and svr3mark == False:
        #     txz_cpu_list.append(0.0)
        #     txzsvr0_cpu_list.append(0.0)
        #     txzsvr1_cpu_list.append(0.0)
        #     txzsvr2_cpu_list.append(0.0)
        #     txzsvr3_cpu_list.append(0.0)
        # if MusicWebchatSwitch:
        #     if musicsvr0 != musicmark:
        #         if not musicmark:
        #             if len(musicsvr0_cpu_list) > len(music_cpu_list):
        #                 music_cpu_list.append(0.0)
        #         if not musicsvr0:
        #             if len(musicsvr0_cpu_list) < len(music_cpu_list):
        #                 musicsvr0_cpu_list.append(0.0)
        #     if playermark != musicmark:
        #         if not musicmark:
        #             if len(musicplayer_cpu_list) > len(music_cpu_list):
        #                 music_cpu_list.append(0.0)
        #         if not playermark:
        #             if len(musicplayer_cpu_list) < len(music_cpu_list):
        #                 musicplayer_cpu_list.append(0.0)
        #     if playermark != musicsvr0:
        #         if not musicsvr0:
        #             if len(musicplayer_cpu_list) > len(musicsvr0_cpu_list):
        #                 musicsvr0_cpu_list.append(0.0)
        #         if not playermark:
        #             if len(musicplayer_cpu_list) < len(musicsvr0_cpu_list):
        #                 musicplayer_cpu_list.append(0.0)
        #     if musicmark == False and musicsvr0 == False and playermark == False:
        #         music_cpu_list.append(0.0)
        #         musicsvr0_cpu_list.append(0.0)
        #         musicplayer_cpu_list.append(0.0)
        #     if not webcahtmark:
        #         webchat_cpu_list.append(0.0)
        # --
        datas.close()
        # return [txzsvr1_cpu_list, txzsvr0_cpu_list, txz_cpu_list, webchat_cpu_list, music_cpu_list,
        #         musicplayer_cpu_list, musicsvr0_cpu_list, txzsvr2_cpu_list, txzsvr3_cpu_list]


# 统计系统总CPU消耗
def statistics_syscpu(data, total_cpu_list):
    Userinfo = re.findall('User.\d+%', data)
    Systeminfo = re.findall('System.\d+%', data)
    if Userinfo:
        total_cpu_list.append(
            int(Userinfo[0].split()[1].replace('%', '')) + int(Systeminfo[0].split()[1].replace('%', '')))


# 统计前5项目
def statistics_top5(data, top5_list, startremind, top5_count):
    global nameinfo
    if data.find('Name') > 0 or startremind:
        while startremind and top5_count:
            top5_count -= 1
            if data.find('root') or data.find('shell') > 0:
                tmp = data[:data.find('root')]
                if tmp.find('fg') > 0 or tmp.find('bg') > 0:
                    index = nameinfo
                else:
                    index = nameinfo - 1
            else:
                index = nameinfo
            try:
                top5_list.append(data.split()[index])
            except:
                localprint('当前行数据异常：' + data + ',long:{0}'.format(len(data)))
            break
        if top5_count == 0:
            return (False, 5)
        else:
            return (True, top5_count)
    else:
        return startremind, top5_count


# 查找CPU/MEM
def exc_search(data, regular, cpu_list):
    search_result = re.findall(regular, data)
    if search_result:
        cpu_list.append(float(search_result[0].strip().split()[cpuinfo].strip('%')))
        return True
    else:
        return False


# 计算APP资源消耗总和
def processall(list1, list2, list3=None, list4=None, list5=None):
    if list5:
        CPUall = np.array(list1) + np.array(list2) + np.array(list3) + np.array(list4) + np.array(list5)
        return list(CPUall.tolist())
    elif list4:
        CPUall = np.array(list1) + np.array(list2) + np.array(list3) + np.array(list4)
        return list(CPUall.tolist())
    elif list3:
        CPUall = np.array(list1) + np.array(list2) + np.array(list3)
        return list(CPUall.tolist())
    else:
        CPUall = np.array(list1) + np.array(list2)
        return list(CPUall.tolist())


# 普通画图---cpu采取补零，导致通过list空的判断失效
def commonanalysedata(env):
    obtianCapabilityinfo(env, amalgamateFile(env, env['top_process_logpath']))
    # if data:
    with open(os.path.join(env['result'], 'cpu.txt'), 'w') as wdata:
        core_cpu_dict = {}
        for process in getObservedLists():
            core_cpu_dict[process] = getProcessInfo(process, key_process_cpu, [])
            pass
        # printInfos()

        wdata.write('core:{0}\n'.format(core_cpu_dict))
        cpu_draw(env, 'txzcore', core_cpu_dict)


# ----------------------------------top_process合成----------------------------------------------------
# top进程数据合成
def amalgamateFile(env, dir):
    filename = os.path.join(env['result'], 'amalgamatefile.txt')
    result = open(filename, 'w')
    for file in os.listdir(dir):
        with open(os.path.join(dir, file)) as datas:
            result.writelines(datas)
        datas.close()
    result.close()
    return filename
