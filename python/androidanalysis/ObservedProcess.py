# -*- coding:utf-8 -*-

# 可观测的对象
# 通过外部传参

# 这是一个集合
observerProcessLists = []


def setObservedLists(lists):
    global observerProcessLists
    if lists != "":
        observerProcessLists = lists.split(";")
    for process in observerProcessLists:
        print process
    # testByMine()
    # testprint()
    # addProcessInfo("com.txznet.txz", "pid", 1234)
    # addProcessInfo("com.txznet.txz", "pid", 1568)
    # addProcessInfo("com.txznet.txz", "time", 1)
    # addProcessInfo("com.txznet.txz:svr0", "time", 1)
    #
    # print getProcessInfo("com.txznet.txz", "pid")
    # print getProcessInfo("com.txznet.txz:svr0", "time")
    # print getProcessInfo("com.txznet.txz:svr0", "pid")
    # print getProcessInfo("com.txznet.txz", "time")
    # print getProcessInfo("com.txznet.txz:svr1", "pid")


def getObservedLists():
    global observerProcessLists
    return observerProcessLists


# 设置一个 dict 列表里面包含 dict dict{processName,dict{${key},[]}} ,key 为 pid kill_time launch
process_dict = {}  # 字典
key_process_pid = "pid"
# key_process_startTime = "start_time"
key_process_stopTime = "stop_time"
key_process_cpu = "cpu"
key_process_mem = "mem"
key_process_begin_mem = "begin_mem"
key_process_end_mem = "end_mem"
key_process_x_coordinate = "x_coordinate"  # x 坐标 在 内存画图中使用
key_process_x_coordinate_base = "x_coordinate_base"  # x 坐标 在 内存画图中使用
key_process_dir = "dir"  # 进程相关的文件夹


def addProcessInfo(processName, key, value):
    if (processName not in process_dict):
        process_dict[processName] = {}
    if (key not in process_dict[processName]):
        process_dict[processName][key] = []  # 列表 # 不可以设置为 set（无序）
    process_dict[processName][key].append(value)


def getProcessInfo(processName, key, default=None):
    if (processName not in process_dict):
        return default
    if (key not in process_dict[processName]):
        return default
    return process_dict[processName][key]


# 判断是否有相应的值
def haveProcessInfo(processName, key, need):
    if (processName not in process_dict):
        return False
    if (key not in process_dict[processName]):
        return False
    for value in process_dict[processName][key]:
        if (value == need):
            return True
    return False


# 这个key 是否 有值
def isNullprocessInfo(processName, key):
    if (processName not in process_dict):
        print("xxxxxx")
        return True
    if (key not in process_dict[processName]):
        print("yyyyyy")
        return True
    return len(process_dict[processName]) == 0


# 获取指定key 长度
def getprocessInfoKeyLen(processName, key):
    if (processName not in process_dict):
        return 0
    if (key not in process_dict[processName]):
        return 0
    return len(process_dict[processName])


hidict = {}  # 字典


def testByMine():
    # hi = map(square, getObservedLists())

    for process in getObservedLists():
        print process
        # 从map中赋值
        # hidict[process] = [1, 23, process]


def testprint():
    global hidict
    for process in getObservedLists():
        if process in hidict:
            hidict[process].append("process：" + process)
            for value in hidict[process]:
                print value


def printInfos():
    if process_dict:
        for key in process_dict:
            print " " + key
            if process_dict[key]:
                for keyvalue in process_dict[key]:
                    print "     " + keyvalue
                    if process_dict[key][keyvalue]:
                        for value in process_dict[key][keyvalue]:
                            print "         " + str(value)
