# -*- coding:utf-8 -*-

import os
import time
import base64
from ObservedProcess import getObservedLists
from ProcessUtils import initProcess

from FileUtils import mkdirs


# 使用设备准备环境变量
# 根据 设备 名称  创建 各种文件夹
def genEnv(dev=None):
    env = {}
    if dev is not None:
        env['dev'] = dev
    if dev is None:
        env['tag'] = time.strftime('%Y%m%d_%H%M%S')
    else:
        # env['tag'] = dev.replace(':','_').replace('？','_').replace('?','_') + '_' + base64.b64encode(dev) + '_' + time.strftime('%Y%m%d_%H%M%S')
        env['tag'] = base64.b64encode(dev) + '_' + time.strftime('%Y%m%d_%H%M%S')

    print env['tag']
    env['dir'] = env['tag']
    os.makedirs(env['dir'])  # 只有一台设备就创建时间名的目录，多台设备就创建含设备编码的目录

    # 循环创建 进程相关的文件夹
    for process in getObservedLists():
        initProcess(env, process)

    env['memmoredata_core'] = os.path.join(env['dir'], 'memmoredata_core')
    os.makedirs(env['memmoredata_core'])

    env['flow'] = os.path.join(env['dir'], 'flow')
    os.makedirs(env['flow'])

    env['result'] = os.path.join(env['dir'], 'Result')
    os.makedirs(env['result'])

    env['memlogpath'] = os.path.join(env['dir'], 'memdata')
    os.makedirs(env['memlogpath'])

    env['top_thread_logpath'] = os.path.join(env['dir'], 'top_thread_data')
    os.makedirs(env['top_thread_logpath'])

    env['top_process_logpath'] = os.path.join(env['dir'], 'top_process_data')
    os.makedirs(env['top_process_logpath'])

    env['syslogpath'] = os.path.join(env['dir'], 'SYSLog')
    os.makedirs(env['syslogpath'])

    env['hprof'] = os.path.join(env['dir'], 'Hprof')
    os.makedirs(env['hprof'])

    env['pullApk'] = os.path.join(env['dir'], 'pullApk')
    os.makedirs(env['pullApk'])

    env['log'] = open(env['dir'] + '/preburning.log', 'w')
    return env
