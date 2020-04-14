# coding:utf-8


def world1():
    print "world"


def world2():
    from androidanalysis.analysis.AnalysisPid import getPidFromPackage
    from androidanalysis.constant.ObservedProcess import setObservedLists
    env = {'dev': "0123456789ABCDEF"}
    setObservedLists("com.txznet.txz:svr6")
    getPidFromPackage(env, "com.txznet.txz:svr6")

    from androidanalysis.analysis.AnalysisPid import pidPro
    import multiprocessing
    _StopMark = multiprocessing.Value('b', False)
    pidPro(env, _StopMark,2)


if __name__ == '__main__':
    world2()
