# -*- coding:utf-8 -*-

from DrawUtils import *
from TimeUtils import *
from adbUtils import *
from ObservedProcess import getObservedLists
from ObservedProcess import getProcessInfo
from ObservedProcess import addProcessInfo
from ObservedProcess import key_process_stopTime
from ObservedProcess import key_process_mem
from ObservedProcess import key_process_x_coordinate
from ObservedProcess import key_process_x_coordinate_base
from ObservedProcess import key_process_begin_mem
from ObservedProcess import key_process_end_mem
from ProcessUtils import get_process
from FileUtils import mkdirs


def memPro(env, _StopMark):
    # global memtimer
    threading.Thread(target=mymem, args=(env, _StopMark)).start()
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
        writeLog(env, "正在写入 {0} 进程的内存 到文件{1}/mem_{2}...".format(process, process_mem_dir, t))
        file1.write(stdoutdata1)
        file1.close()
        del file1
    moredatas.terminate()
    mLock.release()


# 抓取内存数据
def mymem(env, _StopMark):
    # runAdbCommand(env,['connect','127.0.0.1:62001'])
    while True:
        if env['dev'] in readDeviceList():
            writeLog(env, '>>>------------抓取内存数据------------')
            for process in getObservedLists():
                # 抓取指定进程名称的内存信息
                writeProcessMem(env, process)
            writeProcessMem(env)  # 抓取总体的内存信息
        # 休眠1s 继续执行 ，什么时候结束？
        print _StopMark.value
        if _StopMark.value:
            break
        time.sleep(1)
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
    with open(os.path.join(env['result'], 'mem.txt'), 'w') as wdata:
        for process in getObservedLists():
            core_dict = {}
            core_dict[process] = getProcessInfo(process, key_process_mem, [])
            wdata.write('{0}:{1}\n'.format(process, core_dict))
            # print "what:" + str(getProcessInfo(process, key_process_x_coordinate, []))
            mem_draw(env, process, core_dict, adress,
                     getProcessInfo(process, key_process_x_coordinate, []))


def exc_memdata(env):
    global startMark
    global startTime
    startMark = False
    startTime = 0
    adress = env['memlogpath']
    if adress:
        for file in os.listdir(adress):
            myfile = os.path.join(adress, file)
            if os.path.getsize(myfile) < 4 * 1024:
                continue
            excuteMemdata(myfile)

        memDraw(env, adress)
    else:
        writeLog(env, "路径为空，请检查!")


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
    for process in getObservedLists():
        DalvikHeapSizeList = []
        DalvikHeapAllocList = []
        DalvikHeapPssList = []
        DalvikHeapXList = []
        startMark = False
        firstTime = 0
        dir = os.path.join(env['memmoredata_core'], get_process(process))
        for filename in os.listdir(dir):
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
