
 adb push busybox /system/xbin/
 adb root
 adb remount

 adb shell "chmod  755 /system/xbin/busybox"

 adb shell "busybox --install ."

 adb shell "awk"
 adb shell "ps |grep com.txznet.music|awk '{print $2}' | head -n 1"

