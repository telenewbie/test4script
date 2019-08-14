adb pull /sdcard/txz/log/text_all D:/log
if "%1" == "all" (
	for /l %%i in (1,1,10) do adb  pull /sdcard/txz/log/text_all_%%i D:/log/
)
