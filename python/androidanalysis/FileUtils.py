# -*- coding:utf-8 -*-
import os


def closeProc(filemark):
    if not os.path.exists(filemark):
        print '{0} cread'.format(filemark)
        with open(filemark, 'a') as datas:
            datas.close()


# 移除流程控制文件
# stopApkMark successMark
def removeStateFile(filemark):
    if os.path.exists(filemark):
        os.remove(filemark)


def mkdirs(path):
    path = path.replace(":", "_")
    if not os.path.exists(path):
        os.makedirs(path)
