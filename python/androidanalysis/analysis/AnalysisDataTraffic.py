# -*- coding:utf-8 -*-

from androidanalysis.utils.LogFileUtils import *

# 数据流量


uploadFlow = 7
downloadFlow = 5


def flowCounter(env, userid, hour):
    if userid < 0:
        return False
    result = []
    from androidanalysis.utils.osUtils import listdir
    filelist = listdir(env['flow'])
    if len(filelist) > 1:
        for filename in filelist:
            with open(os.path.join(env['flow'], filename)) as mData:
                mDownloadFlow = 0
                mUploadFlow = 0
                for linedata in mData:
                    if linedata.find('lo') >= 0:
                        continue
                    if linedata.find(userid) >= 0:
                        linelist = linedata.split()
                        mDownloadFlow += int(linelist[downloadFlow])
                        mUploadFlow += int(linelist[uploadFlow])
                result.append(mDownloadFlow + mUploadFlow)
                writeLog(env, '{0}  下载流量：{1},上传流量：{2}'.format(filename, mDownloadFlow, mUploadFlow))
        B = float(result[1] - result[0])
        M = B / 1024 / 1024
        writeLog(env, '总共使用{0:.2f}字节，即{1:.2f}兆，平均每小时使用{2:.2f}兆'.format(B, M, M / hour))
