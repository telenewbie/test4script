# coding:utf-8

import os


# 'MDEyMzQ1Njc4OUFCQ0RFRg==_20200316_185041\\memmoredata_core\\com.txznet.music'
# 'build\\result\\top_process_data'
def listdir(path):
    _list = []
    if os.path.exists(path) and os.path.isdir(path):
        _list = os.listdir(path)
        if _list is None:
            _list = []
    return _list
