

setlocal enabledelayedexpansion rem  �����Ƿ���Ҫ���±���ֵ


::pause

for /f  "tokens=1-3 delims=:" %%a in ('adb shell pm list package -3') do (

set dd=%%b
set "dd=!dd:~0,10!"
echo !dd!
echo %%b


rem set PARAM=%%b

rem set "PARAM=!PARAM:~0,10!" rem ע������Ϊ������������:~

rem echo  ���!PARAM!

if not "!dd!" =="com.txznet" call adb uninstall %%b

)


	