# coding:utf-8


def world1():
    print "world"


def world2():
    from AnalysisPid import getPidFromPackage
    from ObservedProcess import setObservedLists
    env = {'dev': "0123456789ABCDEF"}
    setObservedLists("com.txznet.txz:svr6")
    getPidFromPackage(env, "com.txznet.txz:svr6")

    from AnalysisPid import pidPro
    import multiprocessing
    _StopMark = multiprocessing.Value('b', False)
    pidPro(env, _StopMark,2)


if __name__ == '__main__':
    world2()
    # from ObservedProcess import getObservedTypeDict, setObservedLists
    # setObservedLists("com.txznet.txz:svr6")
    # print getObservedTypeDict()
