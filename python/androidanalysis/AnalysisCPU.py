# -*- coding:utf-8 -*-

import traceback

from TimerUtils import *
from adbUtils import *
from SoftwareUtils import *
from ObservedProcess import getObservedLists
from ObservedProcess import key_process_cpu
from ObservedProcess import addProcessInfo
from ObservedProcess import key_process_cpu_x
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
    mytimer(env, _StopMark)  # FIXMe 暂时注释
    timerMark = True
    _top_thread_cmd = ['adb', '-s', env['dev'], 'shell', 'top', '-t', '-d', '1', '-n', '1']
    _top_thread_p = subprocess.Popen(_top_thread_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _syslog_cmd = ['adb', '-s', env['dev'], 'logcat', '-v', 'time']
    _syslog_p = subprocess.Popen(_syslog_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _top_process_cmd = ['adb', '-s', env['dev'], 'shell', 'top', '-d', '1', '-n', '1']
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
    print cpu_info
    count = 0
    with open(file) as datas:
        top5_list = []
        startremind = False
        top5_count = 10

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
                    count += 1
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

                addProcessInfo(data.split()[-1], key_process_cpu, float(data.split()[cpu_info].strip('%')))
                # 通过比较次数

                addProcessInfo(data.split()[-1], key_process_cpu_x, count)
        writeLog(env, 'CPU占用TOP{0}榜单:{1}'.format(top5_count,
                                                 str(collections.Counter(top5_list)).replace('Counter({', '').replace(
                                                     '}', '').replace(': ', ':(').replace(
                                                     ',', '),')))


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
    from ObservedProcess import getObservedTypeDict
    from ObservedProcess import getProcess
    from mergeData import merge_x
    from mergeData import merge_y
    obtianCapabilityinfo(env, amalgamateFile(env, env['top_process_logpath']))
    # if data:
    with open(os.path.join(env['result'], 'cpu.txt'), 'w') as wdata:
        _dict = getObservedTypeDict()
        for _process_list in _dict:
            core_cpu_dict = {}
            _cpu_list_x = []
            for process in _dict[_process_list]:
                _process_dict = getProcess(process)
                if _process_dict is not None:
                    core_cpu_dict[process] = _process_dict
                    _cpu_list_x.append(getProcessInfo(process, key_process_cpu_x, []))

            # 计算总和
            if len(core_cpu_dict) <= 0:
                continue
            _all_x_list = list(merge_x(_cpu_list_x))
            _all_y_list = merge_y(_all_x_list, key_process_cpu_x, key_process_cpu, core_cpu_dict)
            core_cpu_dict["all"] = {}
            core_cpu_dict["all"][key_process_cpu_x] = _all_x_list
            core_cpu_dict["all"][key_process_cpu] = _all_y_list

            wdata.write('core:{0}\n'.format(core_cpu_dict))
            cpu_draw_1(env, "cpu_all", core_cpu_dict, key_process_cpu_x, key_process_cpu)


# ----------------------------------top_process合成----------------------------------------------------
# top进程数据合成
def amalgamateFile(env, dir):
    filename = os.path.join(env['result'], 'amalgamatefile.txt')
    result = open(filename, 'w')
    from osUtils import listdir
    for file in listdir(dir):
        with open(os.path.join(dir, file)) as datas:
            result.writelines(datas)
        datas.close()
    result.close()
    return filename
