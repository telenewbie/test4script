# -*- coding:utf-8 -*-
import time
import os
# from multiprocessing import *
import multiprocessing


def run(name):
    while True:
        time.sleep(2)
        print("子进程ID号:%d，run：%s" % (os.getpid(), name))  # os.getpid()进程ID


if __name__ == "__main__":
    # print("父进程启动：%d" % os.getpid())
    # # 创建子进程
    # p = Process(target=run, args=("Ail",))  # target进程执行的任务, args传参数（元祖）
    # p.start()  # 启动进程
    # while True:
    #     print("死循环")
    #     time.sleep(1)
    num = multiprocessing.Array("i", [1, 2, 3, 4, 5])
