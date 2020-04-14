# coding:utf-8
# 进程相关数据
from androidanalysis.bean import Info

g_info = Info


def get_info():
    global g_info
    return g_info


def set_info(info):
    global g_info
    g_info = info
