# -*- coding:utf-8 -*-
from androidanalysis.analysis.AnalysisCPU import *
from androidanalysis.ObservedProcess import setObservedLists
import multiprocessing
from androidanalysis.utils.envUtils import genEnv

from androidanalysis.config.Constant import setOver


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


def testGetCpu(env):
    _StopMark = multiprocessing.Value('b', False)
    testModel = 1
    excute(env, _StopMark, testModel)


if __name__ == "__main__":
    # obtainindex("Top.log")
    # setObservedLists("com.txznet.music")
    setObservedLists("com.txznet.txz;com.txznet.txz:svr1;com.txznet.txz:svr6")
    # hello()
    # testMem()
    env = {}
    # 这里的路径需要修改
    # env['dir'] = "MDEyMzQ1Njc4OUFCQ0RFRg==_20200316_185041"
    env['dir'] = r"..\..\build\result"
    # env['dev'] = "R804211907020094"


    # env['dev'] = "127.0.0.1:62001"
    env = genEnv(test=True, myenv=env)

    from androidanalysis.ObservedProcess import getObservedTypeDict

    _dict = getObservedTypeDict()
    for process in _dict:
        print _dict[process]

    # testCPU()
    testCPU(env)
    # testprintmem(env)

