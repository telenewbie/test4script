# -*- coding:utf-8 -*-
import os
import subprocess
from threading import Timer
from Constant import *
from Constant import __RE_REMOTE_DEV
from Constant import __RE_IP_ADRESS
from Constant import _RE_TTSAPK
from Constant import __RE_APK_PATH
from Constant import _ENV_PCM
from Constant import _RE_SYSLOGTIME
from Constant import _TXZ_path
from winProcessUtils import *
from logFile import *


# 开启日志
def openlog(env):
    runAdbCommand(env, ['shell', 'mkdir', '-p', _TXZ_path])
    runAdbCommand(env, ['shell', 'touch', _TXZ_path + 'log_enable_file'])
    runAdbCommand(env, ['shell', 'touch', _TXZ_path + 'ENABLE_TRACE_GPS.debug'])
    runAdbCommand(env, ['shell', 'touch', _TXZ_path + 'yzs_log.debug'])
    runAdbCommand(env, ['shell', 'touch', _TXZ_path + 'txz_abc1234321.debug'])
    runAdbCommand(env, ['shell', 'touch', _TXZ_path + 'disable_remote_tts_tool.debug'])
    runAdbCommand(env, ['shell', 'touch', _TXZ_path + 'pcm_enable.debug'])
    runAdbCommand(env, ['shell', 'touch', _TXZ_path + 'disable_remote_set_res.debug'])
    runAdbCommand(env, ['shell', 'touch', _TXZ_path + 'ENABLE_TRACE_NAV_INFO.debug'])
    runAdbCommand(env, ['shell', 'touch', _TXZ_path + 'call_stack_enable'])


def obtaincontent(content):
    # print [content]
    return content


# 运行adb指令
def runAdbCommand(env, cmds, inputs=None, check=None, timeout=None):
    dev = env.get('dev', None)
    if dev is not None:
        cmds = ['adb', '-s', dev] + cmds
    else:
        cmds = ['adb'] + cmds
    return runCommand(env, cmds, inputs, check, timeout)


def runCommand(env, cmds, inputs=None, check=None, timeout=None, count=5):
    if type(inputs) == type([]):
        inputs = '\n'.join(inputs) + '\n'  # inputs重组成字符串
    infd = subprocess.PIPE
    if inputs is not None and type(inputs) != type(''):  # 非空且不是字符串
        infd = inputs
        inputs = None
    # print cmds
    p = subprocess.Popen(cmds, stdin=infd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                         creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    if inputs is not None:
        print inputs

    def kp(_env, _p, _timeout):
        writeLog(_env, '执行过程出现超时: %s' % _timeout)
        killPid(_p.pid)
        _p.returncode = None

    if timeout is not None:
        # writeLog(env, '任务超时设置: %s' % timeout)
        my_timer = Timer(timeout, kp, [env, p, timeout])  # 超时时间，调用方法，传入参数
        my_timer.start()
    else:
        my_timer = None
    stdoutdata, stderrdata = p.communicate(inputs)
    # complete = False
    # timeoutcount = 2400
    # stdoutdata = ''
    # stderrdata = ''
    # while p.poll() == None and timeoutcount >= 0:
    #     time.sleep(0.1)
    #     print p.poll()
    #     print timeoutcount
    #     timeoutcount -= 1
    # else:
    #     if timeoutcount >= 0:
    #         complete = True
    #         stdoutdata, stderrdata = p.communicate(inputs)#向子进程传入inputs参数，等待外部程序执行结束
    # if not complete:
    #     return -1
    # print stderrdata
    # writeLog(env,stdoutdata+stderrdata)
    if my_timer is not None:
        my_timer.cancel()
    ret = p.returncode  # 进程执行状态码，0正常
    if check is not None:
        content = ''
        if stdoutdata is not None:
            content += stdoutdata
        if stderrdata is not None and stderrdata != '':
            content += stderrdata
            writeLog(env, '>>>指令%s,执行过程出现错误: %s' % (' '.join(cmds), stderrdata.strip()))
            # 出现设备未连接错误时，重连再执行
            if stderrdata.find('offline') >= 0 or stderrdata.find('error') >= 0 or stderrdata.find(
                    "ADB server didn't ACK") >= 0 or stderrdata.find("^C") >= 0:
                os.system('adb kill-server')
                os.system('taskkill /f /t /im adb.exe')
                os.system('adb start-server')
                count -= 1
                if count > 0:
                    time.sleep(3)
                    return runCommand(env, cmds, inputs, check, timeout, count)
                else:
                    global errorstauts
                    errorstauts = True
                    return -1
            if stderrdata.find('device') >= 0 and stderrdata.find('not found') >= 0:
                checkConnect(env, False)
                return runCommand(env, cmds, inputs, check, timeout)  # 有检查错误，出现断开连接则重新执行
        r = check(content)
        if r is not None:
            ret = r
    return ret


# 延时 秒
def delayTime(env, t):
    writeLog(env, '延迟等待: %s......' % t)
    time.sleep(t)


# 确认连接
def checkConnect(env, needRoot=True):
    dev = env.get('dev', None)
    n = 1
    if dev is not None and __RE_REMOTE_DEV.match(dev):
        while True:
            writeLog(env, '>>>尝试连接远程设备: %d' % n)
            if runCommand(env, ['adb', 'connect', dev]) == 0: break  # 非test状态无限尝试，直到连接成功
            n += 1
            delayTime(env, 10)
        writeLog(env, '>>>远程设备连接成功')
    else:
        while True:
            writeLog(env, '>>>尝试连接本地设备: %d' % n)
            if runAdbCommand(env, ['shell', 'true']) == 0: break
            n += 1
            delayTime(env, 10)
        writeLog(env, '>>>本地设备连接成功')
    if not needRoot:
        return True
    writeLog(env, '>>>申请adb的root权限')
    obtainRoot(env)
    if dev is not None and __RE_REMOTE_DEV.match(dev):  # 远程连接，获取root后需重新连接
        runAdbCommand(env, ['disconnect', dev])
        checkConnect(env, False)
    return True


# 获取root 权限
def obtainRoot(env):
    cmds = [
        # https://forum.xda-developers.com/android-auto/android-head-units/ownice-c500-released-t3478747/page50
        'forfan guoboneedav',
        'remount',
        'exit',
    ]
    runAdbCommand(env, ['shell'], inputs=cmds)
    runAdbCommand(env, ['root'])
    runAdbCommand(env, ['remount'])


# 读取设备列表
def readDeviceList():
    ret = []
    p = subprocess.Popen(['adb', 'devices'], stdout=subprocess.PIPE)
    outstr, errstr = p.communicate()
    for dev in outstr.splitlines()[1:]:
        if dev.find('devices') >= 0:
            continue
        if dev.find('daemon') > 0:
            continue
        if dev.find('offline') >= 0:
            continue
        if dev.find('client') >= 0:
            continue
        dev = dev.strip()
        n = len(dev)
        while n > 0:
            n -= 1
            if dev[n] == ' ' or dev[n] == '\t':
                break
        if n <= 0: continue
        dev = dev[:n].strip()
        ret.append(dev)
    return ret


# 备份IP地址
def backupIPadress():
    os.system('adb devices')
    ret = []
    p = subprocess.Popen(['adb', 'devices'], stdout=subprocess.PIPE)
    outstr, errstr = p.communicate()
    for dev in outstr.splitlines()[1:]:
        dev = dev.strip()
        dev = __RE_IP_ADRESS.search(dev)
        if dev:
            ret.append(dev.group())
    os.system('adb kill-server')
    for ip in ret:
        os.system('adb connect %s' % ip)


# 通过pid杀应用 通过 ps 获取 指定包名 的 进程号，然后kill pid即可
# FIXME：通过 adb force-stop  包名就可以啊。
def killApkPid(env, apk):
    obtainRoot(env)
    psinfo = runAdbCommand(env, ['shell', 'ps'], check=obtaincontent)
    pid_index = 0
    for partinfo in psinfo.split('\n'):
        if partinfo.find('PID') > 0:
            pid_index = partinfo.split().index('PID')
        txzsearchinfo = re.compile('%s$' % apk).search(partinfo.strip())
        if txzsearchinfo:
            txz_pid = partinfo.split()[pid_index]
            writeLog(env, '>>>当前%s的PID为：%s,将执行kill操作' % (apk, txz_pid))
            runAdbCommand(env, ['shell', 'kill', txz_pid])


# ----------------------------------结果数据处理----------------------------------------------------
# 获取crash文件数量
def obtianCrashCount(env):
    def obtainList(content):
        txzlist = re.findall('crash_com\.txznet\.txz.+', content)
        musiclist = re.findall('crash_com\.txznet\.music.+', content)
        webchatlist = re.findall('crash_com\.txznet\.webchat.+', content)
        return (len(txzlist), len(musiclist), len(webchatlist))

    txzCount, musicCount, webchatCount = runAdbCommand(env, ['shell', 'ls', '/sdcard/txz/report/'], check=obtainList)
    writeLog(env, 'CoreCrash文件{0}个，音乐Crash文件{1}个，微信Crash文件{2}个'.format(txzCount, musicCount, webchatCount))


# 删除crash文件
def deleteOldCrashfile(env):
    runAdbCommand(env, ['shell', 'rm', '/sdcard/txz/report/*'])
    runAdbCommand(env, ['shell', 'rm', '/sdcard/preburning/asr/*'])
    runAdbCommand(env, ['shell', 'rm', '/sdcard/preburning/pcm/*'])

# 取出 现有的 core的apk
def pullInitialAPK(env):
    corePath = runAdbCommand(env, ['shell', 'pm', 'path', 'com.txznet.txz'], check=obtaincontent)
    if corePath != '':
        runAdbCommand(env, ['pull', corePath.split(":")[-1].strip(), env['pullApk']])
    mline = checklog(env, 'start loadRes path:')
    if mline:
        runAdbCommand(env, ['pull', _RE_TTSAPK.findall(mline)[0].strip(), env['pullApk']])


# 准备环境
def prepareDevice(env, _StopMark, curpath):
    writeLog(env, '>>>准备环境')
    obtainRoot(env)
    if not checkenv(env, Preburning, 'preburning.apk', _StopMark):
        return False
    if _StopMark.value:
        return False
    launch_apk(env, 'com.txznet.txz')
    launch_apk(env, 'com.txznet.preburning')
    runAdbCommand(env, ['shell', 'mkdir', '-p', _ENV_PCM + 'pcm'])
    pushfiletoandroid(env, curpath, _ENV_PCM + 'pcm/')
    writeLog(env, 'Current Scene:{0}'.format(curpath))
    runAdbCommand(env, ['push', './command.txt', _ENV_PCM])
    return True


# monkey启动apk
def launch_apk(env, apk):
    if apk == 'com.txznet.txz':
        # 调整“系统”按键事件所占百分比  为 0  即 不会 模拟 按键 。（这些按键通常预留供系统使用，例如“主屏幕”、“返回”、“发起通话”、“结束通话”或“音量控件”。）
        runAdbCommand(env, ['shell', 'monkey', '-p', 'com.txznet.sdkdemo', '--pct-syskeys', '0', '-v', '1'])
        time.sleep(3)
    else:
        runAdbCommand(env, ['shell', 'monkey', '-p', apk, '--pct-syskeys', '0', '-v', '1'])
        time.sleep(3)
    writeLog(env, '>>>monkey启动%s' % apk)


# 检查&安装apk流程
def checkenv(env, apk, apkpath, _StopMark):
    firstcheck = uninstallapk(env, apk)
    if _StopMark.value:
        return False
    if firstcheck == rmsuccess:
        secondcheck = uninstallapk(env, apk)
        if _StopMark.value:
            return False
        if secondcheck == nonexist:
            writeLog(env, '校验移除成功')
            if _StopMark.value:
                return False
            if installapk(env, apk, apkpath):
                writeLog(env, '{0}配置完成'.format(apk))
                return True
            elif installSystemapk(env, apk, apkpath):
                writeLog(env, '{0}配置完成'.format(apk))
                return True
            elif installapk(env, apk, apkpath):
                writeLog(env, '再次尝试install，{0}配置完成'.format(apk))
                return True
            else:
                writeLog(env, '{0}配置失败'.format(apk))
                return False
        elif secondcheck == noroot:
            return norootexecute(env, apk, apkpath)
        elif secondcheck == rmsuccess:
            checkenv(env, apk, apkpath, _StopMark)
        else:
            writeLog(env, '{0}移除失败，需人工处理'.format(apk))
    elif firstcheck == noroot:
        return norootexecute(env, apk, apkpath)
    elif firstcheck == rmfail:
        writeLog(env, '{0}，需人工处理'.format(apk))
        return False
    else:
        writeLog(env, '{0}不存在，无需移除'.format(apk))
        if _StopMark.value:
            return False
        if installapk(env, apk, apkpath):
            writeLog(env, '{0}配置完成'.format(apk))
            return True
        elif installSystemapk(env, apk, apkpath):
            writeLog(env, '{0}配置完成'.format(apk))
            return True
        elif installapk(env, apk, apkpath):
            writeLog(env, '再次尝试install，{0}配置完成'.format(apk))
            return True
        else:
            writeLog(env, '{0}配置失败'.format(apk))
            return False


rmsuccess = 1
rmfail = 2
nonexist = 3
noroot = 4


def uninstallapk(env, apk, count=3):
    result = rmfail
    pathinfo = str(runAdbCommand(env, ['shell', 'pm', 'path', apk], check=obtaincontent))
    if pathinfo:
        if pathinfo.find('/data/') >= 0 or pathinfo.find('{0}-'.format(apk)) >= 0:
            apkpath = __RE_APK_PATH.search(pathinfo.strip()).group().replace(':', '')
            writeLog(env, 'uninstall：{0}'.format(apkpath))
            excresult = runAdbCommand(env, ['uninstall', apk], check=obtaincontent)
            if excresult.find('Success') >= 0:
                writeLog(env, '{0} uninstall Success'.format(apk))
                result = rmsuccess
            else:
                writeLog(env, '{0} uninstall Fail'.format(apk))
                count -= 1
                # 递归删除
                if count > 0:
                    checkConnect(env, False)
                    result = uninstallapk(env, apk, count)
        elif pathinfo.find('/system/') >= 0:
            apkpath = __RE_APK_PATH.search(pathinfo.strip()).group().replace(':', '')
            writeLog(env, 'delete：{0}'.format(apkpath))
            obtainRoot(env)
            excresult = runAdbCommand(env, ['shell', 'rm', '-f', apkpath], check=obtaincontent)
            rebootDevice(env)
            if excresult.find('No such file or directory') >= 0:
                writeLog(env, excresult.strip())
                result = rmfail
            elif excresult.find('Read-only') >= 0:
                writeLog(env, 'Root Fail:{0}'.format(excresult.strip()))
                result = noroot
            else:
                writeLog(env, '{0} delete Success'.format(apk))
                result = rmsuccess
        elif pathinfo.find('/') >= 0:
            writeLog(env, 'unknown format,not execute')
            result = rmfail
        else:
            writeLog(env, '{0} does not exist!'.format(apk))
            result = nonexist
    else:
        writeLog(env, '{0} does not exist!'.format(apk))
        result = nonexist
    return result


def installSystemapk(env, apk, apkpath, count=3):
    result = False
    versioninfo = runAdbCommand(env, ['shell', 'getprop', 'ro.build.version.release'], check=obtaincontent)
    primacy = versioninfo.strip().split('.')
    obtainRoot(env)
    if apk == Core:
        apkname = 'TXZCore.apk'
    elif apk == Preburning:
        apkname = 'preburning.apk'
    else:
        apkname = 'unknown.apk'
    if int(primacy[0]) < 5 or apk != Core:
        writeLog(env, 'Android {0}：push {1}'.format(versioninfo.strip(), system_app_path))
        # print ' '.join(['push',apkpath,system_app_path])
        pushinfo = runAdbCommand(env, ['push', apkpath, system_app_path + apkname], check=obtaincontent)
        if pushinfo.find('100%') >= 0:
            writeLog(env, '{0} push Success'.format(apk))
            rebootDevice(env)
            path = runAdbCommand(env, ['shell', 'pm', 'path', apk], check=obtaincontent)
            if path.find(system_app_path) >= 0:
                result = True
            else:
                result = False
        elif pushinfo.find('Read-only') >= 0:
            writeLog(env, 'Root Fail:doing install')
            result = installapk(env, apk, apkpath, count)
        else:
            writeLog(env, '{0} push Fail'.format(apk))
            count -= 1
            if count > 0:
                checkConnect(env, False)
                result = installSystemapk(env, apk, apkpath, count)
    else:
        writeLog(env, 'Android {0}：push {1}'.format(versioninfo.strip(), core_dev_path))
        runAdbCommand(env, ['shell', 'mkdir', '-p', corelib_dev_path])
        pushinfo = runAdbCommand(env, ['push', apkpath, core_dev_path + apkname], check=obtaincontent)
        if pushinfo.find('100%') >= 0:
            writeLog(env, '{0} push Success'.format(apk))
            rebootDevice(env)
            path = runAdbCommand(env, ['shell', 'pm', 'path', apk], check=obtaincontent)
            if path.find(core_dev_path) >= 0:
                result = True
            else:
                result = False
        elif pushinfo.find('Read-only') >= 0:
            writeLog(env, 'Root Fail:doing install')
            result = installapk(env, apk, apkpath, count)
        else:
            writeLog(env, '{0} push Fail'.format(apk))
            count -= 1
            if count > 0:
                checkConnect(env, False)
                result = installSystemapk(env, apk, apkpath, count)
    return result


def installapk(env, apk, apkpath, count=3):
    result = False
    installinfo = runAdbCommand(env, ['install', '-r', apkpath], check=obtaincontent)
    if installinfo.find('Success') >= 0:
        writeLog(env, '{0} install Success'.format(apk))
        # rebootDevice(env)
        path = runAdbCommand(env, ['shell', 'pm', 'path', apk], check=obtaincontent)
        if path.find('/data/') >= 0 or path.find('/mnt/asec') >= 0:
            result = True
        else:
            result = False
    else:
        writeLog(env, '{0} install Fail'.format(apk))
        count -= 1
        if count > 0:
            checkConnect(env, False)
            result = installapk(env, apk, apkpath, count)
    return result


def norootexecute(env, apk, apkpath):
    path1 = runAdbCommand(env, ['shell', 'pm', 'path', apk], check=obtaincontent)
    if installapk(env, apk, apkpath):
        path2 = runAdbCommand(env, ['shell', 'pm', 'path', apk], check=obtaincontent)
        writeLog(env, 'Pre:{0},Back:{1}'.format(path1.strip(), path2.strip()))
        if path1 != path2:
            writeLog(env, '{0}配置成功'.format(apk))
            return True
        else:
            writeLog(env, '{0}覆盖安装失败，需人工处理'.format(apk))
            return False
    else:
        writeLog(env, '{0}覆盖安装失败，需人工处理'.format(apk))
        return False


def startPreburn(env, testModel, _TimeValue):
    if testModel == 1:  # 音频模式
        if _TimeValue == '':
            # 不带参数，apk默认传1
            runAdbCommand(env, ['shell', 'am', 'broadcast', '-a', 'com.txznet.preburning.start'])
            writeLog(env, '>>>excute:' + ' '.join(['shell', 'am', 'broadcast', '-a', 'com.txznet.preburning.start']))
        else:
            runAdbCommand(env,
                          ['shell', 'am', 'broadcast', '-a', 'com.txznet.preburning.start', '--ei', 'time', _TimeValue])
            writeLog(env, '>>>excute:' + ' '.join(
                ['shell', 'am', 'broadcast', '-a', 'com.txznet.preburning.start', '--ei', 'time', _TimeValue]))
    elif testModel == 2:  # 文本模式
        if _TimeValue == '':
            # model=2文本模式
            runAdbCommand(env, ['shell', 'am', 'broadcast', '-a', 'com.txznet.preburning.start', '--ei', 'model', '2'])
            writeLog(env, '>>>excute:' + ' '.join(
                ['shell', 'am', 'broadcast', '-a', 'com.txznet.preburning.start', '--ei', 'model', '2']))
        else:
            runAdbCommand(env, ['shell', 'am', 'broadcast', '-a', 'com.txznet.preburning.start', '--ei', 'model', '2',
                                '--ei', 'time', _TimeValue])
            writeLog(env, '>>>excute:' + ' '.join(
                ['shell', 'am', 'broadcast', '-a', 'com.txznet.preburning.start', '--ei', 'model', '2', '--ei', 'time',
                 _TimeValue]))
    elif testModel == 3:  # 什么都不做
        pass


# 重启设备
def rebootDevice(env, connect=False, setPlan=False):
    dev = env.get('dev', None)
    writeLog(env, '>>>重启设备')
    runAdbCommand(env, ['reboot'], timeout=10)
    runAdbCommand(env, ['remount'], timeout=10)
    delayTime(env, 50)
    if dev is not None and __RE_REMOTE_DEV.match(dev):
        # 需要先断开连接，否则下一步时连接不会断开
        runAdbCommand(env, ['disconnect', dev])
    ret = checkConnect(env, False)
    # 某些设备的初始化程序用的是sdkdemo
    launch_apk(env, 'com.txznet.txz')
    delayTime(env, 15)
    return ret


# 推送文件到设备
def pushfiletoandroid(env, orgpath, targpaht, suffix='.pcm'):
    for mfile in os.listdir(orgpath):
        if mfile.endswith(suffix) >= 0:
            runAdbCommand(env, ['push', os.path.join(orgpath, mfile),
                                os.path.join(targpaht, mfile.decode('gbk').encode('utf-8'))])


def pullLog(env, log_path):
    writeLog(env, '>>>获取日志文件')
    runAdbCommand(env, ['pull', '/sdcard/txz/report', log_path + '/'])
    runAdbCommand(env, ['pull', '/sdcard/Android/data/com.txznet.txz/files/log/AI/', log_path + '/'])
    pulltxzlog(env, log_path)
    runAdbCommand(env, ['pull', '/sdcard/crash', log_path + '/'])
    runAdbCommand(env, ['pull', '/data/anr', log_path + '/'])
    runAdbCommand(env, ['pull', '/data/tombstones/', log_path + '/'])
    # 皮工，占用资源，可能引起core的自杀，暂不使用
    # obtainHprof(env)
    # obtainMusicHprof(env)


# 抓取txzlog
def pulltxzlog(env, tarpath):
    filelist = runAdbCommand(env, ['shell', 'ls', '/sdcard/txz/log'], check=obtaincontent)
    if isinstance(filelist, str):
        for mfile in filelist.split():
            if mfile.find('text_all') >= 0:
                runAdbCommand(env, ['pull', '/sdcard/txz/log/{0}'.format(mfile), tarpath])
    else:
        print '{0}'.format(filelist)


# 获取上报信息
def getReport(env, action='', Timeing=True):
    global txzlogtimer
    root = env.get('dir', None)
    log_path = os.path.join(root, action + time.strftime('%Y%m%d_%H%M%S'))
    os.makedirs(log_path)
    threading.Thread(target=pullLog, args=(env, log_path)).start()
    if Timeing:
        txzlogtimer = Timer(3600, getReport, (env, 'txzlog_'))
        # txzlogtimer = Timer(1320,getReport,(env,))
        txzlogtimer.start()
    print 'obtain log compeled'
