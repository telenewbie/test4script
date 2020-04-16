# -*- coding:utf-8 -*-

from Tkinter import *
import Queue
import multiprocessing

from PreBurningUtils import *
from FileUtils import *
from androidanalysis.utils.adbUtils import *

import traceback
from androidanalysis.utils.LogFileUtils import *

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
        timeValue = StringVar(value=DEFAULT_INTERVAL_CHANGE_WIFI)
        Label(self.root, text='定时改变wifi状态（ms），默认不启动').grid(row=rowIndex, column=0, sticky='W', columnspan=4)
        Entry(self.root,
              width=30,
              textvariable=timeValue
              ).grid(row=rowIndex, column=3, columnspan=4, sticky='W')
        rowIndex += 1
        global cpu_interval
        cpu_interval = IntVar(value=DEFAULT_INTERVAL_CPU)
        Label(self.root, text='拉取cpu时间间隔（默认{0}s）'.format(cpu_interval.get())).grid(row=rowIndex, column=0, sticky='W',
                                                                                   columnspan=4)
        Entry(self.root,
              width=30,
              textvariable=cpu_interval
              ).grid(row=rowIndex, column=3, columnspan=4, sticky='W')
        rowIndex += 1
        global mem_interval
        mem_interval = IntVar(value=DEFAULT_INTERVAL_MEM)
        Label(self.root, text='拉取内存时间间隔（默认{0}s）'.format(mem_interval.get())).grid(row=rowIndex, column=0, sticky='W',
                                                                                  columnspan=4)
        Entry(self.root,
              width=30,
              textvariable=mem_interval
              ).grid(row=rowIndex, column=3, columnspan=4, sticky='W')
        rowIndex += 1
        global pid_interval
        pid_interval = IntVar(value=DEFAULT_INTERVAL_PID)
        Label(self.root, text='拉取pid fd  task  时间间隔（默认{0}s）'.format(pid_interval.get())).grid(row=rowIndex,
                                                                                                   column=0, sticky='W',
                                                                                                   columnspan=4)
        Entry(self.root,
              width=30,
              textvariable=pid_interval
              ).grid(row=rowIndex, column=3, columnspan=4, sticky='W')
        rowIndex += 1
        global pull_log_interval
        pull_log_interval = IntVar(value=DEFAULT_INTERVAL_PULL_LOG)
        Label(self.root, text='拉取日志时间间隔（默认{0}s）'.format(pull_log_interval.get())).grid(row=rowIndex, column=0,
                                                                                        sticky='W', columnspan=4)
        Entry(self.root,
              width=30,
              textvariable=pull_log_interval
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
        rowIndex += 1  # 7
        global need_pull_core
        need_pull_core = BooleanVar()
        need_pull_core.set(True)
        self.check_pull_core = Checkbutton(self.root,
                                    variable=need_pull_core,
                                    text='取出当前设备core 的apk',
                                    onvalue=True,
                                    offvalue=False,
                                    )
        self.check_pull_core.grid(row=rowIndex, column=0, columnspan=4, sticky='W')
        rowIndex += 1  # 7
        global need_replace_burning_apk
        need_replace_burning_apk = BooleanVar()
        need_replace_burning_apk.set(True)
        self.check_replace_burning = Checkbutton(self.root,
                                    variable=need_replace_burning_apk,
                                    text='替换设备原有的老化工具',
                                    onvalue=True,
                                    offvalue=False,
                                    )
        self.check_replace_burning.grid(row=rowIndex, column=0, columnspan=4, sticky='W')
        rowIndex += 1  # 7
        global need_delete_old_file
        need_delete_old_file = BooleanVar()
        need_delete_old_file.set(True)
        self.check_delete_old_file = Checkbutton(self.root,
                                    variable=need_delete_old_file,
                                    text='每次运行 是否 删除设备原有的crash anr pcm hprof 数据',
                                    onvalue=True,
                                    offvalue=False,
                                    )
        self.check_delete_old_file.grid(row=rowIndex, column=0, columnspan=4, sticky='W')

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
                    self.check_pull_core['state'] = DISABLED
                    self.check_replace_burning['state'] = DISABLED
                    self.check_delete_old_file['state'] = DISABLED
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
                    self.check_pull_core['state'] = NORMAL
                    self.check_replace_burning['state'] = NORMAL
                    self.check_delete_old_file['state'] = NORMAL
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


write_pipe = []
from androidanalysis.bean.Info import Info

info = Info()


def mainProc(_StopMark):
    # _TimeValue = timeValue.get().strip()
    _StopMark.value = False
    # testModel = testModelVar.get()
    # _processNames = processNames.get().strip()
    # _switchMode = switchModeVar.get()
    # _intervalVar = intervalVar.get()
    info.wifi_change_interval = timeValue.get().strip()
    info.mode = testModelVar.get()
    info.process_names = processNames.get().strip()
    info.need_replace_burning_apk = need_replace_burning_apk.get()
    info.need_pull_core_apk = need_pull_core.get()
    info.need_delete_old_file = need_delete_old_file.get()

    if not switchModeVar.get():
        info.change_pcm_list_interval = 0
    if not intervalVar.get():
        info.change_pcm_interval = 0
    try:
        info.interval_pull_log = int(pull_log_interval.get())
        info.interval_mem = int(mem_interval.get())
        info.interval_cpu = int(cpu_interval.get())
        info.interval_pid_fd_task = int(pid_interval.get())
    except ValueError:
        pass

    # 完全没有必要，自己搞定 adb device
    # backupIPadress()
    # time.sleep(3)

    deviceList = readDeviceList()
    if deviceList:
        for dev in deviceList:
            info.dev = dev
            print '============begin test: ' + dev
            # 使用管道进行进程间通讯
            # 创建管道
            recv_conn, write_conn = multiprocessing.Pipe()
            write_pipe.append(write_conn)

            p = multiprocessing.Process(target=child_process,
                                        args=(_StopMark, recv_conn))
            p.start()
            write_conn.send(info)
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
