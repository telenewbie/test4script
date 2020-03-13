# -*- coding:utf-8 -*-

from Tkinter import *
import Queue
import multiprocessing
from threading import Timer
import os
from PreBurningUtils import *
from Constant import *
from FileUtils import *
from adbUtils import *

import traceback
from logFile import *
from Constant import setOver

my_stop = multiprocessing.Value('b', False)


class GuiPart(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.root = parent
        self.queue = Queue.Queue()
        rowIndex = 1
        self.root.title("老化自动测试工具")
        Label(self.root, text='测试建议：从三个方面无网络（设备启动时就已经处于无网络状态），有网络，频\n繁切换网络进行测试\n' +
                              '分两次进行测试：(1)测试无网络及有网络。设备无网启动，wifi切换设置16200000\n（即4.5H）进行测试' +
                              '(2)频繁切网络。wifi切换设置180000（即3min）进行测试', justify='left', fg='red').grid(row=rowIndex,
                                                                                                   column=0, sticky='W',
                                                                                                   columnspan=22)
        rowIndex += 1
        Label(self.root, text='观测的进程名称 英文符号<;>进行分割').grid(row=rowIndex, column=0, sticky='W', columnspan=4)
        rowIndex += 1
        global processNames
        processNames = StringVar(value="com.txznet.txz;com.txznet.txz:svr1")
        Entry(self.root,
              width=60,
              textvariable=processNames
              ).grid(row=rowIndex, column=0, columnspan=22, sticky='W')
        rowIndex += 1  # 3
        Label(self.root, text='老化执行模式:').grid(row=rowIndex, column=0, sticky='W')
        # 进行core版本
        global testModelVar
        testModelVar = IntVar()
        testModelVar.set(1)
        Radiobutton(self.root, text='音频模式', variable=testModelVar, value=1).grid(row=rowIndex, column=1, sticky='W')
        Radiobutton(self.root, text='文本模式', variable=testModelVar, value=2).grid(row=rowIndex, column=2, sticky='W')
        Radiobutton(self.root, text='什么都不做', variable=testModelVar, value=3).grid(row=rowIndex, column=3, sticky='W')

        rowIndex += 1  # 4
        global timeValue
        timeValue = StringVar()
        Label(self.root, text='定时改变wifi状态（ms），默认不启动').grid(row=rowIndex, column=0, sticky='W', columnspan=4)
        Entry(self.root,
              width=30,
              textvariable=timeValue
              ).grid(row=rowIndex, column=3, columnspan=4, sticky='W')

        # global waitVar
        rowIndex += 1  # 5
        self.waitVar = BooleanVar()
        self.waitVar.set(True)
        self.keep = Checkbutton(self.root,
                                variable=self.waitVar,
                                text='停止测试后，是否保持10分钟静态数据抓取',
                                onvalue=True,
                                offvalue=False,
                                )
        self.keep.grid(row=rowIndex, column=0, columnspan=4, sticky='W')

        rowIndex += 1  # 6
        global switchModeVar
        switchModeVar = BooleanVar()
        switchModeVar.set(False)
        self.switchMode = Checkbutton(self.root,
                                      variable=switchModeVar,
                                      text='音频模式下，是否启动音频集切换，2小时切换一个音频集',
                                      onvalue=True,
                                      offvalue=False,
                                      )
        self.switchMode.grid(row=rowIndex, column=0, columnspan=4, sticky='W')

        rowIndex += 1  # 7
        global intervalVar
        intervalVar = BooleanVar()
        intervalVar.set(False)
        self.interval = Checkbutton(self.root,
                                    variable=intervalVar,
                                    text='切换音频集模式下，是否间隔5分钟',
                                    onvalue=True,
                                    offvalue=False,
                                    )
        self.interval.grid(row=rowIndex, column=0, columnspan=4, sticky='W')

        rowIndex += 2  # 9
        self._StopMark = multiprocessing.Value('b', False)
        # print 'ui:'+str(self._StopMark.value)
        EXC_button = Button(self.root,
                            text='开始测试',
                            command=lambda: preburning_start(self.queue, self._StopMark),
                            # command = beginTest,
                            )
        EXC_button.grid(row=rowIndex, column=1)
        self.exc_button = EXC_button

        Stop_button = Button(self.root,
                             text='停止测试',
                             command=lambda: preburning_stop(self.queue),
                             state=DISABLED
                             )
        Stop_button.grid(row=rowIndex, column=3)
        self.stop_button = Stop_button
        self.periodicCall()

    def periodicCall(self):
        self.master.after(200, self.periodicCall)
        self.processIncoming()
        if os.path.exists(successMark):
            os.remove(successMark)
            self.queue.put('stop')

    def processIncoming(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                if msg == 'start':
                    self.exc_button['state'] = DISABLED
                    self.stop_button['state'] = NORMAL
                    self.keep['state'] = DISABLED
                    self.switchMode['state'] = DISABLED
                    self.interval['state'] = DISABLED
                if msg == 'stop_transfer':
                    if self.waitVar.get():
                        closeProc(stopApkMark)
                        Timer(60 * 10, stop, (self,)).start()
                    else:
                        stop(self)
                    self.stop_button['state'] = DISABLED
                if msg == 'stop':
                    self.exc_button['state'] = NORMAL
                    self.keep['state'] = NORMAL
                    self.switchMode['state'] = NORMAL
                    self.interval['state'] = NORMAL
                    self.stop_button['state'] = DISABLED
            except Queue.Empty:
                traceback.print_exc()
                pass


def stop(self):
    self._StopMark.value = True


def preburning_start(mQueue, _StopMark):
    mQueue.put('start')
    threading.Thread(target=mainProc, args=(_StopMark,)).start()


def preburning_stop(mQueue):
    mQueue.put('stop_transfer')
    global my_stop
    my_stop.value = True


def mainProc(_StopMark):
    _StopMark.value = False
    testModel = testModelVar.get()
    _TimeValue = timeValue.get().strip()
    _processNames = processNames.get().strip()

    _switchMode = switchModeVar.get()
    _intervalVar = intervalVar.get()
    backupIPadress()
    time.sleep(3)
    deviceList = readDeviceList()
    if deviceList:
        for dev in deviceList:
            print '============begin test: ' + dev
            p = multiprocessing.Process(target=beginTest,
                                        args=(
                                            _StopMark, _processNames, _TimeValue, _switchMode, _intervalVar, testModel,
                                            dev))
            p.start()
        print 'mainProc End'
    else:
        closeProc(successMark)
        print 'no devices'


def createGui():
    global root
    root = Tk()
    root.wm_resizable(False, False)
    client = GuiPart(root)
    pass


def showGui():
    root.mainloop()
    pass
