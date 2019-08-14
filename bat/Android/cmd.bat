@echo off
rem if 条件与括号之间有空格
rem 判断bat是否传递了参数使用"%1" == ""


setlocal EnableDelayedExpansion
:loop
echo.*----------------------------------*
echo.*---1 .杀掉同听进程----------------*
echo.*---2 .杀掉Core进程----------------*
echo.*---3 .杀掉SDKDemo进程-------------*
echo.*---4 .删掉同听的所有缓存----------*
echo.*---5 .拉取text_all日志------------*
echo.*---6 .拉取全部日志----------------*
echo.*---7 .设置支持busybox-------------*
echo.*---8 .测试是否支持busybox---------*
echo.*---9 .截屏------------------------*
echo.*---10.输入密码--------------------*
echo.*---11.卸载非同行者相关的APK-------*
echo.*---12.卸载同听--------------------*
echo.*---13.一键安装所有设定的apk-------*

set /P choice=
echo.你选择了%choice%
if "%choice%" == "1" (
	call python killMusicProcess.py com.txznet.music
	echo."成功执行"
)
if "%choice%" =="2" (
	call python killMusicProcess.py com.txznet.txz
	echo."成功执行"
)
if "%choice%" =="3" (
	call python killMusicProcess.py com.txznet.sdkdemo
	echo."成功执行"
)
if "%choice%" =="4" (
	call 清理电台之家的所有缓存文件.bat
	echo."成功执行"
)
if "%choice%" =="5" (
	call 拉取日志.bat
	echo."成功执行"
)
if "%choice%" =="6" (
	call 拉取日志.bat all
	echo."成功执行"
)
if "%choice%" =="7" (
	call 设置busybox.bat
	echo."成功执行"
)
if "%choice%" =="8" (
	call python testSettingbusybox.py
	echo."成功执行"
)
if "%choice%" =="9" (
	call screencap.bat
	echo."成功执行"
)
if "%choice%" =="10" (
	call txz密码.bat
	echo."成功执行"
)
if "%choice%" =="11" (
	call 卸载除同行者产品之外的apk.bat
	echo."成功执行"
)
if "%choice%" =="12" (
	call 卸载Audio.bat
	echo."成功执行"
)
if "%choice%" =="13" (
	call 一键安装所有的软件.bat
	echo."成功执行"
)
if "%choice%" =="0" (
	goto end
)
set "choice="
pause
goto loop
:end
