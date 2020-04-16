# coding:utf-8
import subprocess
import time
import os
from androidanalysis.utils.LogFileUtils import writeLog
import thread


def start_get_sys_log(env, _stop_mark):
    thread.start_new_thread(get_sys_log, (env, _stop_mark))


def get_sys_log(env, _stop_mark):
    # 设置系统文件的大小 512K
    single_file_size = 512 * 1024
    easytime = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    syslog_file_name = 'SYS_%s.log' % (easytime)
    _syslog_cmd = ['adb', '-s', env['dev'], 'logcat', '-v', 'time']
    _syslog_p = subprocess.Popen(_syslog_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open(os.path.join(env['syslogpath'], syslog_file_name), 'wb') as syslog_file:
        # 重复写入数据
        while True:
            # 如果 点击停止则退出
            if _stop_mark.value:
                write_with_popen(env, _syslog_p, syslog_file, env['syslogpath'], syslog_file_name, _syslog_cmd, True)
                return
            _syslog_p, syslog_file = write_with_popen(env, _syslog_p, syslog_file, env['syslogpath'], syslog_file_name,
                                                 _syslog_cmd)
            syslog_file.write(_syslog_p.stdout.readline().strip() + '\n')
            if syslog_file.tell() >= single_file_size:
                syslog_file.flush()
                syslog_file.close()
                get_sys_log(env, _stop_mark)
                return
        pass

# 清理出现异常的进程
# closeObtain 更名为 writeWithPOpen
def write_with_popen(env, p, log_file, logpath, logfilename, cmd, killmark=False):
    import traceback
    if p.poll() != None or killmark:
        a = p.stdout.flush()
        if a != None:
            try:
                log_file.write(a)
            except:
                writeLog(env, traceback.print_exc())
                log_file.close()
                log_file = open(os.path.join(logpath, logfilename), 'wb')
                log_file.write(a)
        if not killmark:
            return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE), log_file
        else:
            return None, log_file
    return p, log_file
