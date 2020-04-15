# -*- coding:utf-8 -*-

from ProcessUtils import get_process_fd
from ProcessUtils import get_process_fd_path
from ProcessUtils import get_process_task
from ProcessUtils import get_process_task_path
from androidanalysis.utils.adbUtils import *


# 获取索引
def obtainindex(file):
    global cpu_info
    # global memoryinfo_rss
    # global nameinfo
    with open(file) as datas:
        for data in datas:
            if data.find('PCY') > 0:
                titlelist = data.strip().split()
                if len(titlelist) > 12:
                    memoryinfo_rss = titlelist.index('RSS') - 2
                    nameinfo = titlelist.index('Name') - 2
                else:
                    memoryinfo_rss = titlelist.index('RSS')
                    nameinfo = titlelist.index('Name')
                cpu_info = titlelist.index('CPU%')
                break
        datas.close()
    return cpu_info, memoryinfo_rss, nameinfo
    # print cpu_info
    # print memoryinfo_rss
    # print nameinfo


# 获取fd
def obtainfd(env, t, pid, item):
    datas = subprocess.Popen(['adb', '-s', env['dev'], 'shell', 'ls', '-al', '/proc/{0}/fd'.format(pid)],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                             creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    stdoutdata, stderrdata = datas.communicate()
    with open(os.path.join(get_process_fd_path(env, item), get_process_fd(item) + t + r'.txt'), 'w') as mfile:
        mfile.write(stdoutdata)
        # writeLog(env, '{1} FdCount:{0}'.format(len(stdoutdata.strip().split('\n')), item))
        mfile.close()
        del mfile
    datas.terminate()


# 获取task
def obtaintask(env, t, pid, item):
    with open(os.path.join(get_process_task_path(env, item), get_process_task(item) + t + r'.txt'), 'w') as mfile:
        idlist = runAdbCommand(env, ['shell', 'ls', '/proc/{0}/task/'.format(pid)], check=obtaincontent).strip().split()
        for mId in idlist:
            mfile.write(str(runAdbCommand(env, ['shell', 'cat', '/proc/{0}/task/{1}/comm'.format(pid, mId)],
                                          check=obtaincontent)).strip() + '\n')
        mfile.close()
        del mfile


def obtainuserid(env):
    def obtainUserId(content):
        mContent = content.strip()
        if mContent.find('userId') >= 0:
            return mContent.split()[0].split('=')[1]
        else:
            writeLog(env, 'userId 获取失败')
            return -1

    return runAdbCommand(env, ['shell', 'dumpsys', 'package', 'com.txznet.txz', '|', 'findstr', 'userId'],
                         check=obtainUserId)
