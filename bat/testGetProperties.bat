REM 打印出给定的文件的相关属性

echo off
echo path name:
echo %1
echo fully qualified path name:
echo %~f1
echo dirive:
echo %~d1
echo path:
echo %~p1
echo name:
echo %~n1
echo extention:
echo %~x1
echo short name:
echo %~s1
echo attribute:
echo %~a1
echo time:
echo %~t1
echo size:
echo %~z1
echo directory:
echo %~dp1


pause