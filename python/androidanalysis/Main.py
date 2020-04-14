# -*- coding:utf-8 -*-
import sys

# 可以直接使用命令行执行 https://stackoverflow.com/questions/15514593/importerror-no-module-named-when-trying-to-run-python-script
sys.path.append('../')

from androidanalysis.utils.GUIUtils import *

if __name__ == "__main__":
    createGui()
    showGui()
