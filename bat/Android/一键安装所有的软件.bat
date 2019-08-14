rem 安装所有的apk底下的所有apk文件
@echo off
setlocal enabledelayedexpansion
 

for /R "G:\learnScript\apk" %%s in (*) do ( 
	set str=%%s
	echo "adb install !str!"
	adb install !str!
)
 pause