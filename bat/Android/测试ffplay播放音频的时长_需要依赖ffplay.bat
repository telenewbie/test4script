echo 开始时间：%time%
set beginTime=%time:~0,2%%time:~3,2%%time:~6,2%
ffplay https://audio.leting.io/dedbb65b-e411-4663-b8df-e69170f1c101.m4a


set endTime= %time:~0,2%%time:~3,2%%time:~6,2%
set /A spendTime=%endTime%-%beginTime%
echo 共花费了%spendTime%
pause