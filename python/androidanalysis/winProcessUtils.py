# -*- coding:utf-8 -*-

import os
import time
import base64
import threading
import ctypes
import sys

# windows 管理进程
TH32CS_SNAPPROCESS = 0x00000002
class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [("dwSize", ctypes.c_ulong),
                 ("cntUsage", ctypes.c_ulong),
                 ("th32ProcessID", ctypes.c_ulong),
                 ("th32DefaultHeapID", ctypes.c_ulong),
                 ("th32ModuleID", ctypes.c_ulong),
                 ("cntThreads", ctypes.c_ulong),
                 ("th32ParentProcessID", ctypes.c_ulong),
                 ("pcPriClassBase", ctypes.c_ulong),
                 ("dwFlags", ctypes.c_ulong),
                 ("szExeFile", ctypes.c_char * 260)]

def getProcList():
    CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
    Process32First = ctypes.windll.kernel32.Process32First
    Process32Next = ctypes.windll.kernel32.Process32Next
    CloseHandle = ctypes.windll.kernel32.CloseHandle
    hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    pe32 = PROCESSENTRY32()
    pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
    if Process32First(hProcessSnap,ctypes.byref(pe32)) == False:
        print >> sys.stderr, "Failed getting first process."
        return
    while True:
        yield pe32
        if Process32Next(hProcessSnap,ctypes.byref(pe32)) == False:
            break
    CloseHandle(hProcessSnap)

def getChildPid(pid):
    procList = getProcList()
    for proc in procList:
        if proc.th32ParentProcessID == pid:
            yield proc.th32ProcessID

#杀掉进程的进程树
def killPid(pid):
    childList = getChildPid(pid)
    for childPid in childList:
        killPid(childPid)
    handle = ctypes.windll.kernel32.OpenProcess(1, False, pid)
    ctypes.windll.kernel32.TerminateProcess(handle,0)