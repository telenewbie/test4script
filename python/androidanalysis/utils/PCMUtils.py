# -*- coding:utf-8 -*-
import os

from osUtils import listdir


def obtainPcmList(path="."):
    pcmlist = []
    from androidanalysis.utils.CodeUtils import get_decode_str
    for mFile in listdir(path):
        if os.path.isdir(os.path.join(path, mFile)):
            if mFile.lower().find('pcm') >= 0:
                pcmlist.append(get_decode_str(os.path.join(path, mFile)))
    return pcmlist


if __name__ == '__main__':
    obtainPcmList("..")
