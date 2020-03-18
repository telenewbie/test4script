# -*- coding:utf-8 -*-

import os
import time
import base64
from ObservedProcess import getObservedLists
from ProcessUtils import initProcess
from FileUtils import mkdirs



# 使用设备准备环境变量
# 根据 设备 名称  创建 各种文件夹
def genEnv(dev=None, test=False, myenv={}):
    if test:
        env = myenv
    else:
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
    print env['dir']

    mkdirs(env['dir'])  # 只有一台设备就创建时间名的目录，多台设备就创建含设备编码的目录

    # 循环创建 进程相关的文件夹
    for process in getObservedLists():
        initProcess(env, process)

    env['memmoredata_core'] = os.path.join(env['dir'], 'memmoredata_core')
    mkdirs(env['memmoredata_core'])

    env['flow'] = os.path.join(env['dir'], 'flow')
    mkdirs(env['flow'])

    env['result'] = os.path.join(env['dir'], 'Result')
    mkdirs(env['result'])

    env['memlogpath'] = os.path.join(env['dir'], 'memdata')
    mkdirs(env['memlogpath'])

    env['top_thread_logpath'] = os.path.join(env['dir'], 'top_thread_data')
    mkdirs(env['top_thread_logpath'])

    env['top_process_logpath'] = os.path.join(env['dir'], 'top_process_data')
    mkdirs(env['top_process_logpath'])

    env['syslogpath'] = os.path.join(env['dir'], 'SYSLog')
    mkdirs(env['syslogpath'])

    env['hprof'] = os.path.join(env['dir'], 'Hprof')
    mkdirs(env['hprof'])

    env['pullApk'] = os.path.join(env['dir'], 'pullApk')
    mkdirs(env['pullApk'])

    env['log'] = open(env['dir'] + '/preburning.log', 'w')
    return env
