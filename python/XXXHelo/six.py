# coding:utf-8

import subprocess

# 1.
ftest1 = subprocess.Popen('adb shell cd sdcard/Android/data &&ls', stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)  # 使用&&来进行连续的操作
print ftest1.stdout.read()

# 2.
cmds = [
    'pm uninstall com.txznet.music',
    'exit', # 这一步很重要
]
# stdin=subprocess.PIPE 这个很重要 ，输入，输出，错误，交给谁接管的问题
p = subprocess.Popen("adb shell", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
cmds = '\n'.join(cmds) + '\n'
print cmds
outstr, errstr = p.communicate(cmds)
print '-' * 20
print outstr
print errstr.decode("gbk").encode("utf-8")
