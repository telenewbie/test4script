# -*- coding:utf-8 -*-
from SoftwareUtils import *
from AnalysisCPU import *
from ObservedProcess import getProcessInfo
from ObservedProcess import setObservedLists
from ObservedProcess import key_process_dir
from FileUtils import mkdirs
import multiprocessing
import ctypes
from envUtils import genEnv

from Constant import setOver


def hello():
    # global nameinfo
    with open("Top.log") as datas:
        lines = (line.strip() for line in datas)
        space_line_count = 0  # 空行
        data_line = 0
        for data in lines:
            if not data:  # 空行
                # print "空行" + str(space_line_count)
                if data_line > 0:
                    space_line_count = 0
                    data_line = 0
                space_line_count += 1
            elif data:
                # print "非空行" + str(space_line_count)
                data_line = 1
                if space_line_count > 1:
                    continue
                print data
                # print space_line_count
                # print data.split()[-1]


def over1():
    isOver = True


def over2():
    isOver = False


def over3():
    global isOver
    isOver = True


def over4():
    global isOver
    isOver = False


def over5():
    time.sleep(10)
    setOver(True)


def printOver():
    print "local：" + str(isOver)


def printGlobalOver():
    global isOver
    print "global:" + str(isOver)


def globalsettingvar():
    # over1()
    # printOver()
    # printGlobalOver()
    # over2()
    # printOver()
    # printGlobalOver()
    # over3()
    # printOver()
    # printGlobalOver()
    # over4()
    # printOver()
    # printGlobalOver()
    pass


def testprintmem(env):
    # 设置10s后自动关闭
    # threading.Thread(target=over5).start()
    # 开始获取pid 供mem 使用
    # obtainpid(env, 1)
    # 开始打印mem
    memTrend(env)  # 测试通过
    # 通过dumpsys meminfo 的数据都画在一张图上
    exc_memdata(env)
    # 分别绘制各自的内存数据 都 各自的图上
    memoryAnalysis(env)


def testCPU(env):
    commonanalysedata(env)
    obtianCrashCount(env)
    pass


if __name__ == "__main__":
    # obtainindex("Top.log")
    setObservedLists("com.txznet.music")
    # setObservedLists("com.txznet.txz;com.txznet.txz:svr1;com.txznet.music")
    # hello()
    # testMem()
    env = {}
    # 这里的路径需要修改
    env['dir'] = "MDEyMzQ1Njc4OUFCQ0RFRg==_20200316_185041"
    env['dev'] = "127.0.0.1:62001"
    env = genEnv(test=True, myenv=env)

    from ObservedProcess import getObservedTypeDict

    _dict = getObservedTypeDict()
    for process in _dict:
        print _dict[process]

    # testCPU()
    testCPU(env)
    testprintmem(env)
    # # env['dir'] = "MTI3LjAuM_151447"
    #
    # # 测试cpu 测试通过
    # env['top_process_logpath'] = os.path.join(env['dir'], 'top_process_data')
    # env['result'] = os.path.join(env['dir'], 'Result')
    # commonanalysedata(env) # 通过
    #
    # # 测试内存
    # env['memlogpath'] = os.path.join(env['dir'], 'memdata')
    # env['memmoredata_core'] = os.path.join(env['dir'], 'memmoredata_core')
    # # os.mkdir(r"""hello:a""")  # 冒号是盘符
    # for process in getObservedLists():
    #     initProcess(env, process)
    #
    # env['dev'] = "127.0.0.1:62001"
    # # setOver(True)
    # # 初步结论，不同的文件对于同一个变量 即使是global的形态也不会改变另一个文件的值
    # exc_memdata(env)  # 通过
    # testprintmem()
    # # obtainHprof(env,"end")
    # # mytimer(env)
    # # androidanalysis/MTI3LjAuMC4xOjYyMDAx_20200312_181249
    # memTrend(env)
    # memoryAnalysis(env)
    # _StopMark = multiprocessing.Value(ctypes.c_bool, False)
    #
    # excute(env, _StopMark, 1)
