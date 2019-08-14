

setlocal enabledelayedexpansion rem  设置是否需要更新变量值


::pause

for /f  "tokens=1-3 delims=:" %%a in ('adb shell pm list package -3') do (

set dd=%%b
set "dd=!dd:~0,10!"
echo !dd!
echo %%b


rem set PARAM=%%b

rem set "PARAM=!PARAM:~0,10!" rem 注意这里为！！和这里是:~

rem echo  输出!PARAM!

if not "!dd!" =="com.txznet" call adb uninstall %%b

)


	