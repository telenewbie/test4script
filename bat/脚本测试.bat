��@echo off��
rem ����ע���㿴�Ķ���

rem %1
if "%1"=="a" goto end
echo  ʧ��



if ERRORLEVEL 0 echo  haha

for /f "tokens=1-3 delims=," %%a in ("1,2,10") do echo a=%%a b=%%b c=%%c

setlocal enabledelayedexpansion rem  �����Ƿ���Ҫ���±���ֵ


::pause

for /f  "tokens=1-3 delims=:" %%a in ('adb shell pm list package -3') do (

set dd=%%b
set "dd=!dd:~0,10!"
echo !dd!


rem set PARAM=%%b

rem set "PARAM=!PARAM:~0,10!" rem ע������Ϊ������������:~

rem echo  ���!PARAM!

if not "!dd!" =="com.txznet" call uninstallAll.bat %%b

)


adb uninstall "com.txznet.music"
	