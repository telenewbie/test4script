
SOS=`find build__x86_64 -name *.so`
for item in $SOS
do
    echo ======= $item
    objdump -Tt $item |grep IjkMediaPlayer_reset
done

