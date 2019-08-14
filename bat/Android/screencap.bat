@echo off
echo ¿ªÊ¼½ØÍ¼
adb shell screencap -p /sdcard/sc.png
adb pull /sdcard/sc.png D:/log
