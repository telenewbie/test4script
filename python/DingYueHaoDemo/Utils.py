# encoding:utf-8
import time


def timeStamp(t):
    return int(t * 1000)


def getCurrentTimestamp():
    return timeStamp(time.time() * 1000)
