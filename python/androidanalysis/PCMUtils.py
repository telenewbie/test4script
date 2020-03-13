# -*- coding:utf-8 -*-
import os
import subprocess

def obtainPcmList():
    pcmlist = []
    for mFile in os.listdir('.'):
        if os.path.isdir(mFile):
            if mFile.lower().find('pcm') >= 0:
                pcmlist.append(mFile)
    return pcmlist