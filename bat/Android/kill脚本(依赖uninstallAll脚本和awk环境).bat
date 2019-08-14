 setlocal enabledelayedexpansion
 for /f %%a in ('adb shell "ps|grep com.txznet.music|awk '{print $2}'"') do (
 set str=%%a
 echo !str!
 set c=!str:~0,5!
 echo !c!
 adb shell kill !c!
 )
 adb shell "ps|grep com.txznet.music|awk '{print $2}'"
pause
