@echo off
echo ��ʼ��ͼ
adb shell screencap -p /sdcard/sc.png
adb pull /sdcard/sc.png D:/log
