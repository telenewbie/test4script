# -*- coding:utf-8 -*-

import threading

from androidanalysis.constant.ObservedProcess import addProcessInfo
from androidanalysis.constant.ObservedProcess import getObservedLists
from androidanalysis.constant.ObservedProcess import getProcess
from androidanalysis.constant.ObservedProcess import getProcessInfo
from androidanalysis.constant.ObservedProcess import key_process_begin_mem
from androidanalysis.constant.ObservedProcess import key_process_end_mem
from androidanalysis.constant.ObservedProcess import key_process_mem
from androidanalysis.constant.ObservedProcess import key_process_stopTime
from androidanalysis.constant.ObservedProcess import key_process_x_coordinate
from androidanalysis.constant.ObservedProcess import key_process_x_coordinate_base
from androidanalysis.utils.DrawUtils import *
from androidanalysis.utils.FileUtils import mkdirs
from androidanalysis.utils.ProcessUtils import get_process
from androidanalysis.utils.TimeUtils import *
from androidanalysis.utils.adbUtils import *


def memPro(env, _StopMark, interval=60):
    # global memtimer
    threading.Thread(target=mymem, args=(env, _StopMark, interval)).start()
    # memtimer = Timer(1, memPro, (env,))
    # memtimer.start()


mLock = threading.Lock()


def writeProcessMem(env, process=''):
    moredatas = subprocess.Popen(['adb', '-s', env['dev'], 'shell', 'dumpsys', 'meminfo', process],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                 creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    stdoutdata1, stderrdata1 = moredatas.communicate()  # 向子进程传入inputs参数，等待外部程序执行结束
    mLock.acquire()
    # preprocessName = process.replace(":", "_")
    t = time.strftime('%Y-%m-%d_%H%M%S', time.localtime())
    # 创建文件夹
    if process == "":
        process_mem_dir = env['memlogpath']
    else:
        process_mem_dir = os.path.join(env['memmoredata_core'], get_process(process))

    mkdirs(process_mem_dir)

    with open(os.path.join(process_mem_dir, r'mem_' + t + r'.txt'), 'w') as file1:
        # writeLog(env, "正在写入 {0} 进程的内存 到文件{1}/mem_{2}...".format(process, process_mem_dir, t))
        file1.write(stdoutdata1)
        file1.close()
        del file1
    moredatas.terminate()
    mLock.release()


# 抓取内存数据
def mymem(env, _StopMark, interval):
    # runAdbCommand(env,['connect','127.0.0.1:62001'])
    while True:
        if env['dev'] in readDeviceList():
            writeLog(env, '>>>------------抓取内存数据------------')
            for process in getObservedLists():
                # 抓取指定进程名称的内存信息
                writeProcessMem(env, process)
            writeProcessMem(env)  # 抓取总体的内存信息
        # 休眠1s 继续执行 ，什么时候结束？
        if _StopMark.value:
            break

        time.sleep(interval)
    writeLog(env, ">>>------------抓取内存数据------------ 完成")


def memTrend(env):
    killtime = 0
    for process in getObservedLists():
        # 取出最小值
        process_info = getProcessInfo(process, key_process_stopTime)
        if process_info is not None:
            stop_time_lists = sorted(process_info)  # 排序 从 小到大
            if killtime == 0 or killtime > stop_time_lists[0]:
                killtime = stop_time_lists[0]
            pass
        pass
    # writeLog(env, "killtime:" + str(killtime))
    mlist = []
    if killtime != 0:
        killtime = realKillTime(killtime)
        # writeLog(env, "realtime:" + str(killtime))
        for root, dirs, files in os.walk(env['memlogpath']):
            if root == env['memlogpath']:  # 获取当前目录底下的
                for file in files:
                    fileTime = time_pattern.search(file).group()
                    if fileTime < killtime:
                        mlist.append(file)
        if mlist:
            excuteTrend(env, env['memlogpath'], mlist[0], mlist[-1])
    else:
        for root, dirs, filelist in os.walk(env['memlogpath']):
            if root == env['memlogpath']:
                mlist = filelist
                break
            pass

        # print mlist
        if mlist:
            excuteTrend(env, env['memlogpath'], mlist[0], mlist[-1])


def excuteTrend(env, path, startFile, endFile):
    obtainMemInfo(os.path.join(path.decode('utf-8').encode('gbk'), startFile), key_process_begin_mem)
    obtainMemInfo(os.path.join(path.decode('utf-8').encode('gbk'), endFile), key_process_end_mem)
    writeLog(env, startFile)
    writeLog(env, endFile)

    consumeHourValue = consumeMin(testTime(startFile, endFile))
    if not consumeHourValue:
        writeLog(env, 'kill时间点异常，起始就发生kill')
        return
    writeLog(env, "本次统计的数据{0} 到 {1}".format(startFile, endFile))
    for process in getObservedLists():
        begin_mem = getProcessInfo(process, key_process_begin_mem, [0])[0]
        end_mem = getProcessInfo(process, key_process_end_mem, [0])[0]
        ratio = rakeRatio(begin_mem, end_mem, consumeHourValue)
        writeLog(env, "{0} 进程 ----起始内存：{1:.2f}MB，结束内存：{2:.2f}MB，斜率：{3}".format(process, begin_mem, end_mem, ratio))


def obtainMemInfo(file, keyName):
    with open(file, 'a+') as datas:
        txz_meminfo = re.compile("(\\d+?) kB: (\\S+?) \(pid (\\d+?)( / \\S+?)?\)")
        setProcesslist = set()
        lines = (line.replace(',', '') for line in datas)
        for dumpsysinfo in lines:
            txzmem = txz_meminfo.search(dumpsysinfo)
            if txzmem:
                if txzmem.group(2) not in setProcesslist:  # index 从1 开始 txzmem.group(2) 为进程名称
                    # 已经设置过的不用在设置了
                    setProcesslist.add(txzmem.group(2))
                    addProcessInfo(txzmem.group(2), keyName, float(txzmem.group(1)) / 1024)
                    # 计算时间
                    # if getProcessInfo(txzmem.group(2), key_process_x_coordinate) is None:  # 差值
            pass
        datas.close()


corestartTime = 0
webcahtstartTime = 0
musicstartTime = 0
launcherstartTime = 0
coremark = False
webcahtmark = False
musicmark = False
launchermark = False


def excuteMemData(process_name, filename, mem_size):
    addProcessInfo(process_name, key_process_mem, float(mem_size) / 1024)
    if getProcessInfo(process_name, key_process_x_coordinate_base) is None:  # 差值
        addProcessInfo(process_name, key_process_x_coordinate_base, filenametime(filename))
        addProcessInfo(process_name, key_process_x_coordinate, 0)
    else:
        # 取出值进行加减 然后在保存
        mylist = getProcessInfo(process_name, key_process_x_coordinate_base)  # 这里只会用到最后一个没有必要存放这么多

        endtime = filenametime(filename)
        starttime = mylist[0]
        deltime = endtime - starttime
        # addProcessInfo(process_name, key_process_x_coordinate_base, filenametime(filename))
        addProcessInfo(process_name, key_process_x_coordinate, deltime)
        pass


# 将所有的数据都放置再各自的内存中 并分好类别
def excuteMemdata(file):
    filename = os.path.basename(file)
    with open(file, 'a+') as datas:
        txz_meminfo = re.compile("(\\d+?) kB: (\\S+?) \(pid (\\d+?)( / \\S+?)?\)")
        setProcesslist = set()
        lines = (line.replace(',', '') for line in datas)
        for dumpsysinfo in lines:
            txzmem = txz_meminfo.search(dumpsysinfo)
            if txzmem:
                if txzmem.group(2) not in setProcesslist:  # index 从1 开始 txzmem.group(2) 为进程名称
                    # 已经设置过的不用在设置了
                    setProcesslist.add(txzmem.group(2))
                    addProcessInfo(txzmem.group(2), key_process_mem, float(txzmem.group(1)) / 1024)
                    # 计算时间
                    # key_process_x_coordinate_base
                    if getProcessInfo(txzmem.group(2), key_process_x_coordinate_base) is None:  # 差值
                        addProcessInfo(txzmem.group(2), key_process_x_coordinate_base, filenametime(filename))
                        addProcessInfo(txzmem.group(2), key_process_x_coordinate, 0)
                    else:
                        # 取出值进行加减 然后在保存
                        mylist = getProcessInfo(txzmem.group(2), key_process_x_coordinate_base)  # 这里只会用到最后一个没有必要存放这么多

                        endtime = filenametime(filename)
                        starttime = mylist[0]
                        deltime = endtime - starttime
                        # addProcessInfo(txzmem.group(2), key_process_x_coordinate_base, filenametime(filename))
                        addProcessInfo(txzmem.group(2), key_process_x_coordinate,
                                       deltime)
                        pass

            pass
        datas.close()


def memDraw(env, adress):
    from androidanalysis.constant.ObservedProcess import getObservedTypeDict
    from androidanalysis.utils.mergeDataUtils import merge_x
    from androidanalysis.utils.mergeDataUtils import merge_y_1
    with open(os.path.join(env['result'], 'mem.txt'), 'w') as wdata:
        _dict = getObservedTypeDict()
        for _process_list in _dict:
            core_dict = {}
            _cpu_list_x = []
            for process in _dict[_process_list]:
                _process_dict = getProcess(process)
                if _process_dict is not None:
                    core_dict[process] = _process_dict
                    _cpu_list_x.append(getProcessInfo(process, key_process_x_coordinate, []))

            # 计算总和
            if len(core_dict) <= 0:
                continue
            _all_x_list = list(merge_x(_cpu_list_x))
            # _all_y_list = merge_y(_all_x_list, key_process_x_coordinate, key_process_mem, core_dict)
            _all_y_list = merge_y_1(_all_x_list, key_process_x_coordinate, key_process_mem, core_dict)
            core_dict["all"] = {}
            core_dict["all"][key_process_x_coordinate] = _all_x_list
            core_dict["all"][key_process_mem] = _all_y_list

            wdata.write('{0}:{1}\n'.format(process, core_dict))

            # 需要进行分类绘制
            mem_draw_1(env, "mem_all", core_dict, key_process_x_coordinate, key_process_mem)


def exc_memdata(env):
    global startMark
    global startTime
    startMark = False
    startTime = 0
    adress = env['memlogpath']
    from androidanalysis.utils.osUtils import listdir
    if adress:
        success_get_all_mem = True
        for file in listdir(adress):
            myfile = os.path.join(adress, file)
            if os.path.getsize(myfile) < 4 * 1024:
                # 表明没有获取到数据，要么能获取到，要么获取不到
                # 如果 小于 4k 表明获取不到，采用单独进程 adb shell dumpsys meminfo processName的方式进行
                success_get_all_mem = False
                break
            excuteMemdata(myfile)
        if not success_get_all_mem:
            # 从各自的进程里面取获取内存数据
            doMemAnalysis(env)
            pass

        memDraw(env, adress)
    else:
        writeLog(env, "路径为空，请检查!")


def doMemAnalysis(env):
    # 根据 进程名称进入 相应的进程目录下面
    from androidanalysis.utils.osUtils import listdir
    for process in getObservedLists():
        dir = os.path.join(env['memmoredata_core'], get_process(process))
        for filename in listdir(dir):
            if filename is None or filename == '':
                print "helloxxxxxxxxxxxxxxx"
                continue
            with open(os.path.join(dir, filename)) as memData:
                for line in memData:
                    # 如果包含  "TOTAL:" 则 提取出后面的关键字
                    if "TOTAL:" in line:
                        values = line.split(" ")
                        i = 0
                        for value in values:
                            if value.strip() == "":
                                continue
                            i += 1
                            if i == 2:
                                excuteMemData(process, filename, value)
                                # print ",value:" + value
                        pass
                    pass
        pass
    pass


logtime_pattern = re.compile('\d+-\d+-\d+_\d+')


def filenametime(stringvalue):
    logTime = logtime_pattern.search(stringvalue).group()
    # print logTime
    # mem_2017-09-21_212032
    timeArray = time.strptime(logTime, "%Y-%m-%d_%H%M%S")
    return time.mktime(timeArray)


def x(valuemark, startmark, filename, starttime, mlist):
    # if valuemark:
    if not startmark:
        mlist.append(0)
        starttime = filenametime(filename)
        startmark = True
    else:
        mValue = int(filenametime(filename) - starttime)
        if mValue < 0:
            print "what!!!WTF"
        mlist.append(mValue)
    return starttime, startmark


# 可能存在不匹配的情况
PssIndex = 3
HeapAlloc = 7
HeapFree = 8
HeapSize = 6


# 统计com.txznet.txz 的 Dalvik Heap 这一项的占用
def memoryAnalysis(env):
    from androidanalysis.utils.osUtils import listdir
    for process in getObservedLists():
        DalvikHeapSizeList = []
        DalvikHeapAllocList = []
        DalvikHeapPssList = []
        DalvikHeapXList = []
        startMark = False
        firstTime = 0
        dir = os.path.join(env['memmoredata_core'], get_process(process))
        for filename in listdir(dir):
            if filename is None or filename == '':
                print "helloxxxxxxxxxxxxxxx"
                continue
            with open(os.path.join(dir, filename)) as memData:
                for line in memData:
                    if line.find('Dalvik Heap') >= 0:
                        firstTime, startMark = DalvikHeapX(startMark, filename, firstTime, DalvikHeapXList)
                        DalvikHeapList = line.split()
                        DalvikHeapPssList.append(int(DalvikHeapList[PssIndex]))
                        DalvikHeapAllocList.append(int(DalvikHeapList[HeapAlloc]))
                        # print DalvikHeapList[HeapFree]
                        DalvikHeapSizeList.append(int(DalvikHeapList[HeapSize]))
        memoryAnalysisDraw(env, process, dir,
                           DalvikHeapSizeList, DalvikHeapAllocList, DalvikHeapPssList,
                           DalvikHeapXList)


def memoryAnalysisDraw(env, processName, adress, sizelist, alloclist, psslist, xlist):
    if sizelist:
        heapsize_dict = {}
        heapsize_dict['heapsize'] = sizelist
        mem_draw(env, processName + '_heapsize', heapsize_dict, adress, xlist, 'KB')
    if alloclist:
        heapalloc_dict = {}
        heapalloc_dict['heapalloc'] = alloclist
        mem_draw(env, processName + '_heapalloc', heapalloc_dict, adress, xlist, 'KB')
    if alloclist and psslist:
        allocpss_dict = {}
        allocpss_dict['heapalloc'] = alloclist
        allocpss_dict['pss'] = psslist
        mem_draw(env, processName + '_allocpss', allocpss_dict, adress, xlist, 'KB')


def DalvikHeapX(startmark, filename, starttime, mlist):
    if not startmark:
        mlist.append(0)
        starttime = filenametime(filename)
        startmark = True
    else:
        if int(filenametime(filename) - starttime) < 0:
            print line
        mlist.append(int(filenametime(filename) - starttime))
    return starttime, startmark
