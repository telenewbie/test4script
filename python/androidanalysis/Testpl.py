# -*- coding:utf-8 -*-

import pylab as pl
from DrawUtils import mem_draw_1
from FileUtils import mkdirs
import numpy as np
from mergeData import *

if __name__ == '__main__':
    # 画图
    env = {}
    env['result'] = "a"
    mkdirs(env['result'])

    _dict = {}
    _dict["a"] = {}
    _dict["a"]["y"] = [4, 3, 2]
    _dict["a"]["x"] = [1, 3, 9]
    _dict["b"] = {}
    _dict["b"]["y"] = [4, 3, 2, 4]
    _dict["b"]["x"] = [1, 2, 4, 8]
    _dict["c"] = {}
    _dict["c"]["y"] = [1, 2, 3, 4]
    _dict["c"]["x"] = [1, 2, 3, 4]
    _dict["d"] = {}
    _dict["d"]["y"] = [4, 3, 2, 4]
    _dict["d"]["x"] = [4]
    _dict["e"] = {}
    _dict["e"]["b"] = [4, 3, 2, 4]
    _dict["e"]["x"] = [1, 2, 4, 8]

    _list = []
    _list.append(_dict["a"]["x"])
    _list.append(_dict["b"]["x"])
    x_list = list(merge_x(_list))
    print "x 的集合：" + str(x_list)
    y_list = merge_y(x_list, 'x', 'y', _dict)
    print "y 的集合：" + str(y_list)
    all_dict = {"all": {}}
    all_dict["all"]["x"] = x_list
    all_dict["all"]["y"] = y_list

    mem_draw_1(env, "hello", all_dict, "x", "y")
    pass
