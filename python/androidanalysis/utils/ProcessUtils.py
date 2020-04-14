# -*- coding:utf-8 -*-
import os
from FileUtils import mkdirs


def get_process(process):
    return process.replace(":", "_")


def get_process_task(process):
    return process.replace(":", "_") + key_process_task


def get_process_task_path(env, process):
    return env[process + key_process_task]


def get_process_fd_path(env, process):
    return env[process + key_process_fd]


def get_process_fd(process):
    return process.replace(":", "_") + key_process_fd


key_process_task = "_task"
key_process_fd = "_fd"


# key_process_task = "task"

# 初始化 进程相关的变量
def initProcess(env, process):
    env[process] = os.path.join(env['dir'], get_process(process))
    env[process + key_process_task] = os.path.join(env[process], key_process_task)
    env[process + key_process_fd] = os.path.join(env[process], key_process_fd)

    # 创建文件夹
    mkdirs(env[process])
    mkdirs(env[process + key_process_task])
    mkdirs(env[process + key_process_fd])
    pass
