# -*- coding:utf-8 -*-
import os

from osUtils import listdir


def obtainPcmList():
    pcmlist = []
    for mFile in listdir("."):
        if os.path.isdir(mFile):
            if mFile.lower().find('pcm') >= 0:
                pcmlist.append(mFile)
    return pcmlist
