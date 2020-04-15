# -*- coding: utf-8 -*-

# 通过 /proc/pid/stat 和 /proc/pid/task/tid/stat  来获取瞬时进程cpu的情况
# 通过两个瞬时状态 的差值就可以算出 cpu的单位时间的使用率 del_process_cpu
# 通过 /proc/stat  算出 总共的cpu耗时 del_cpu_total
# 通过 del_process_cpu/del_cpu_total *100 就可以算出单核下的 cpu使用率

import os
import re
import threading
import time

ADB = "adb shell"
RE_PKG = re.compile(r'^\w+(\.\w+)+(?::\w+)?$')
cpu_size = 0


def runAdbCmd(cmd):
    return os.popen(ADB + ' ' + cmd).read()


def getPidInfo(lock, pid):
    cpus = runAdbCmd('cat /proc/%s/stat' % pid)
    # print("start get pid:", pid)
    return get_info(cpus, need_full_name=True)


def get_info(usage, ret=None, need_full_name=False):
    # 获取 进程名称 括号内
    # ret = {}
    if ret is None:
        ret = {}
    if len(usage) <= 0:
        return
    # 这是个坑，如果 名称过长会自动截断，所以 取到的是被截断的值
    left = usage.find("(")
    right = usage.find(")")
    if left == -1 and right == -1:
        # print "find name error: ", usage
        return
    pid = usage[:left - 1]
    name = usage[left + 1:right]  # 左右括号内为进程名

    if need_full_name:
        # 这里如果是存在空格 会有问题的
        name = runAdbCmd('cat /proc/%s/cmdline' % pid.strip()).strip(b'\x00'.decode())
    cpus = usage[right + 2:].split(" ")  # 去掉 右括号和空格 开始切割
    base = -2  # 因为将前面两个元素裁剪出去了
    cpu_usr = cpus[base + 13]
    cpu_sys = cpus[base + 14]
    cpu_child_usr = cpus[base + 15]
    cpu_child_sys = cpus[base + 16]
    sum = int(cpu_usr) + int(cpu_sys) + int(cpu_child_usr) + int(cpu_child_sys)
    ret[name] = {'pid': int(pid), 'name': name, 'cpu_usr': int(cpu_usr), 'cpu_sys': int(cpu_sys),
                 "cpu_child_usr": int(cpu_child_usr),
                 "cpu_child_sys": int(cpu_child_sys), "sum": sum}
    return ret


def getPidThreadCpuInfo(lock, pid):
    cpus = re.split("[ |\n]", runAdbCmd('ls /proc/%s/task/' % pid))
    cpus = [x for x in cpus if len(x.strip())]
    ret = {}
    for thread_cpu in cpus:
        usage = runAdbCmd('cat /proc/%s/task/%s/stat' % (pid, thread_cpu))
        # print("start get pid", pid, " tid:", thread_cpu)
        get_info(usage, ret)
    return ret


def getAllCpuInfo(lock):
    ret = {}
    cpus = runAdbCmd('cat /proc/stat').split("\n")[0].split(" ")
    # lock.acquire()
    sum = 0
    items = []
    for cpu in cpus:
        if cpu.strip().isdigit():
            sum += int(cpu)
            items.append(cpu)
    ret = {"item": items, "sum": sum}
    # 将这个写道文件中
    # lock.release()
    return ret


def getCpuSize():
    '''
    计算核心数
    :return:
    '''
    num = runAdbCmd("grep -c 'processor' /proc/cpuinfo")
    # print "hello cpu num :" + num
    return num


def start_monitor_pid_cpu_usage(lock, retrive, pid, doing=None):
    # while True:
    if pid <= 0:
        print ("进程号错误")
        return
    retall_1 = getAllCpuInfo(lock)
    ret1 = getPidInfo(lock, pid)
    time.sleep(retrive)
    retall_2 = getAllCpuInfo(lock)
    # 从无到有 ，在睡眠之后 进程退出了，理论上，获取不到cpu的使用状态，统一按0 算
    ret2 = getPidInfo(lock, pid)

    if ret2 is None:
        # 如果第二次为空 则可能由于 进程退出导致的。所以强制改成 空数据
        ret2 = {}
    if retall_2 is None:
        retall_2 = {}
    write2file(ret1, ret2, retall_1, retall_2, doing=doing)
    # time.sleep(1)


def start_monitor_thread_cpu_usage(lock, retrive, pid, doing=None):
    # while True:
    retall_1 = getAllCpuInfo(lock)
    ret1 = getPidThreadCpuInfo(lock, pid)
    time.sleep(retrive)
    retall_2 = getAllCpuInfo(lock)
    ret2 = getPidThreadCpuInfo(lock, pid)
    write2file(ret1, ret2, retall_1, retall_2, pid, doing)

    # time.sleep(1)


def write2file(ret1, ret2, ret_all1, retall_2, parent_pid=0, doing=None):
    if ret1 is None:
        return
    # assert (ret1 is not None)
    # assert (ret2 is not None)
    assert (ret_all1 is not None)
    assert (retall_2 is not None)

    # global cpu_size
    # if cpu_size == 0:
    #     cpu_size = getCpuSize()

    for process, thread_usage in ret1.items():
        if process in ret2:  # 同时包含在 另一次抓取的才算
            del_process_cpu = 100.0 * (int(ret2[process]["sum"]) - int(ret1[process]["sum"])) / (
                    int(retall_2["sum"]) - int(ret_all1["sum"]))
            del_process_cpu = "%0.2f" % del_process_cpu
            if doing is not None:
                doing(process, parent_pid, ret1[process]["pid"], del_process_cpu)

            # result = runAdbCmd('cat /proc/%s/cmdline' % ret1[process]["pid"])
            # # result = runAdbCmd('cat /proc/%s/cmdline' % 31546)
            # print result
            # print "name:%s parent_pid:%s,pid:%s cpu_usage:%s" % (
            #     process, parent_pid, ret1[process]["pid"], del_process_cpu)


def getPidInfoThreads(interval, pids):
    lock = threading.Lock()
    ths = []
    for pid in pids:
        t = threading.Thread(target=start_monitor_pid_cpu_usage, args=(lock, interval, pid))
        ths.append(t)
        t.start()
        # t1 = threading.Thread(target=start_monitor_thread_cpu_usage, args=(lock, interval, pid))
        # ths.append(t1)
        # t1.start()
    for t in ths:
        t.join()


def cpu_usage(process, time=1):
    '''
    计算 cpu使用率
    :param time: 耗时 ，单位 秒 默认为1秒
    :return:返回 cpu使用率
    u0_a106      12736   236 9 18:36:41 ?     00:14:51 com.txznet.txz
u0_a106      12793   236 22 18:36:42 ?    00:38:18 com.txznet.txz:svr1
u0_a109      13108   236 0 18:37:08 ?     00:00:23 com.txznet.preburning
u0_a106      28059   236 0 20:38:31 ?     00:00:04 com.txznet.txz:svr0
    '''
    # 使用线程池进行 获取
    # threadpool.makeRequests(getPidInfo())

    pids = {
        31546,
        # 12736,
        # 13108,
        # 28059
    }

    getPidInfoThreads(1, pids)
    pass


if __name__ == '__main__':
    # _top_process_p = subprocess.Popen(['adb', 'shell'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # _top_process_p.communicate("cat /proc/stat& ex")
    # cmds = ["cat /proc/stat",
    #         "exit"
    #         ]
    # code = _top_process_p.communicate("\n".join(cmds) + "\n");
    # print _top_process_p.stdout.flush()

    # print code

    cpu_usage("")
    # start_monitor_thread_cpu_usage("", 1, 1941)
