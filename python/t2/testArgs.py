from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
import platform
import sys
import subprocess
import os


def get_args():
    parser = ArgumentParser()
    # 必填项，按顺序 为参数赋予意义
    parser.add_argument('url', help='description')
    # 可选项 需要增加 前缀 才可以 ，规则 "--xxx" 参数名 就是 这里指定的名称
    parser.add_argument("--symfile", help="description")
    # 可选项 这里的 名称就是 后面指定的这个 "--symbol",注意两杠和一杠的区别
    parser.add_argument("-s", "--symbol", help="description")
    # 可选项 和上面的一致
    parser.add_argument("-t", dest="target", help="description")
    return parser.parse_args()


def test1():
    args = get_args()
    url = args.url
    url1 = args.symfile
    url2 = args.symbol
    url3 = args.target
    print(url)
    print(url1)
    print(url2)
    print(url3)


def print_and_run_cmd(cmd):
    return os.system(cmd)


def disable_verity_check():
    verity_output = subprocess.check_output("adb   wait-for-device disable-verity", shell=True)
    if "already" not in verity_output and "disable-verity" not in verity_output and verity_output != "":
        print_and_run_cmd("adb   wait-for-device reboot")
        print_and_run_cmd("adb   wait-for-device root")


LE_DEVICE = 0


def adb_remount(dev_num):
    adb_details = subprocess.check_output('adb -s ' + dev_num + ' wait-for-device version', shell=True)
    adb_version_number = adb_details[29:35]  # getting the adb version number
    if adb_version_number >= "1.0.33" and LE_DEVICE != 1:  # disable_verity_check is applicable from 1.0.33 and above versions
        disable_verity_check()
    if LE_DEVICE:
        os.system('adb -s ' + dev_num + ' wait-for-device shell mount -o,remount rw /')
    else:
        print_and_run_cmd('adb -s ' + dev_num + ' wait-for-device remount')


def check():
    adb_details = subprocess.check_output('adb wait-for-device shell cat /sys/devices/soc0/serial_number', shell=True)
    print(adb_details)
    # adb_version_number = adb_details[29:35]
    # print(adb_version_number)


if __name__ == '__main__':
    check()
