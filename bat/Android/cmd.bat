@echo off
rem if ����������֮���пո�
rem �ж�bat�Ƿ񴫵��˲���ʹ��"%1" == ""


setlocal EnableDelayedExpansion
:loop
echo.*----------------------------------*
echo.*---1 .ɱ��ͬ������----------------*
echo.*---2 .ɱ��Core����----------------*
echo.*---3 .ɱ��SDKDemo����-------------*
echo.*---4 .ɾ��ͬ�������л���----------*
echo.*---5 .��ȡtext_all��־------------*
echo.*---6 .��ȡȫ����־----------------*
echo.*---7 .����֧��busybox-------------*
echo.*---8 .�����Ƿ�֧��busybox---------*
echo.*---9 .����------------------------*
echo.*---10.��������--------------------*
echo.*---11.ж�ط�ͬ������ص�APK-------*
echo.*---12.ж��ͬ��--------------------*
echo.*---13.һ����װ�����趨��apk-------*

set /P choice=
echo.��ѡ����%choice%
if "%choice%" == "1" (
	call python killMusicProcess.py com.txznet.music
	echo."�ɹ�ִ��"
)
if "%choice%" =="2" (
	call python killMusicProcess.py com.txznet.txz
	echo."�ɹ�ִ��"
)
if "%choice%" =="3" (
	call python killMusicProcess.py com.txznet.sdkdemo
	echo."�ɹ�ִ��"
)
if "%choice%" =="4" (
	call �����̨֮�ҵ����л����ļ�.bat
	echo."�ɹ�ִ��"
)
if "%choice%" =="5" (
	call ��ȡ��־.bat
	echo."�ɹ�ִ��"
)
if "%choice%" =="6" (
	call ��ȡ��־.bat all
	echo."�ɹ�ִ��"
)
if "%choice%" =="7" (
	call ����busybox.bat
	echo."�ɹ�ִ��"
)
if "%choice%" =="8" (
	call python testSettingbusybox.py
	echo."�ɹ�ִ��"
)
if "%choice%" =="9" (
	call screencap.bat
	echo."�ɹ�ִ��"
)
if "%choice%" =="10" (
	call txz����.bat
	echo."�ɹ�ִ��"
)
if "%choice%" =="11" (
	call ж�س�ͬ���߲�Ʒ֮���apk.bat
	echo."�ɹ�ִ��"
)
if "%choice%" =="12" (
	call ж��Audio.bat
	echo."�ɹ�ִ��"
)
if "%choice%" =="13" (
	call һ����װ���е����.bat
	echo."�ɹ�ִ��"
)
if "%choice%" =="0" (
	goto end
)
set "choice="
pause
goto loop
:end
