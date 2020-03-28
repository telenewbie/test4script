
import os
import sys
import re
import time
import threading

ADB = "adb shell"
RE_PID = re.compile(r'^\d+$')
RE_SPACE = re.compile('\s+')
RE_PKG = re.compile(r'^\w+(\.\w+)+(?::\w+)?$')
#RE_PKG = re.compile(r'^(com.txznet.txz|com.txznet.adapter)(?::\w+)?$')

def runAdbCmd(cmd):
    return os.popen(ADB + ' ' + cmd).read()

def getAllPidByPkg():
    ps = runAdbCmd('ps').splitlines()
    pids = {}
    for p in ps:
        pinfo = RE_SPACE.split(p)
        if not RE_PKG.match(pinfo[-1]): continue
        pids[pinfo[1]] = {'pid':pinfo[1], 'name': pinfo[-1]}
        #print pinfo
    return pids
        
def getAllPids():
    pids = []
    for pid in runAdbCmd('ls /proc').splitlines():
        if not RE_PID.match(pid): continue
        pids.append(pid)
    return pids


def getPidInfo(ret, lock, pid):
    name = runAdbCmd('cat /proc/%s/cmdline' % pid).split('\0')[0]
    if not RE_PKG.match(name): return
    cpus = runAdbCmd('cat /proc/%s/stat' % pid).split(' ')
    if len(cpus) < 15: return
    cpu_usr = cpus[13]
    cpu_sys = cpus[14]
    lock.acquire()
    ret[pid] = {'pid':pid, 'name':name, 'cpu_usr':cpu_usr, 'cpu_sys':cpu_sys}
    lock.release()


def getPidInfoThreads(infos, pids):
    lock = threading.Lock()
    ths = []
    for pid in pids:
        t = threading.Thread(target=getPidInfo,args=(infos, lock, pid))
        ths.append(t)
        t.start()
    for t in ths:
        t.join()

def getPidInfoBacth(infos, pids):
    cmdstr = ' cat '
    for pid in pids.keys():
        cmdstr += ' /proc/%s/stat ' % pid
    for dat in runAdbCmd(cmdstr).splitlines():
        cpus = dat.split(' ')
        if len(cpus) < 15: continue
        pid = cpus[0]
        info = infos[pid] = pids[pid]
        info['cpu_usr'] = cpus[13]
        info['cpu_sys'] = cpus[14]

def getAllPidInfo():
    t_begin = time.time()
    infos = {}
    method = 2
    #方法一
    if method == 1:
        pids = getAllPids()
        getPidInfoThreads(infos, pids)
    #方法二
    elif method == 2:
        pids = getAllPidByPkg()
        getPidInfoBacth(infos, pids)
    #方法三
    elif method == 3:
        pids = getAllPidByPkg()
        getPidInfoThreads(infos, pids.keys())
    t_end = time.time()
    t_cost = t_end-t_begin
    print 'Cost: %s' % t_cost
    for info in infos.values():
        print '%s , ' % info
    return t_cost, infos

#sys.exit(0)

print ("按回车开始捕获第1次")
raw_input()
infos1 = getAllPidInfo()


print ("按回车开始捕获第2次")
raw_input()
infos2 = getAllPidInfo()




