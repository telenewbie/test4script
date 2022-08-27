# -*- coding: utf-8 -*-

import re

CODE_FILE_OVER = -100
CODE_FAULT_WAKE = -1
CODE_REPEAT_WAKE = -2
CODE_UNKNOWN = -3
MISTAKE_TIME_MS = 300

# 主唤醒词 ID
IDX_MAIN = 0
# 免唤醒词 非0
IDX_FREE_WAKE = 100

## 文件的时间点
file_time_ms = {
    "aec_wakeup-asr.pcm": 3767735,
    "aec_w-wakeup-asr.pcm": 3744573,
    "quiet_L1_wakeup_asr.pcm": 342990,
}


class TAG_WORDS:
    def __init__(self, filename):
        print(f"{self} init!!")
        # try:
        self.fp = open(filename, "r", encoding='UTF-8')
        self.fp.seek(0)
        # xxx = self.fp.readline()
        # print(f"hello world {xxx}")
        self.shouldWakeWordCount = 0
        self.wakeWordTimeRange = []
        self.repeatWakeWordIndex = 0
        self.repeatWakeRage = []
        self.lastStartIndex = 0
        self.lastEndIndex = 0
        # except:
        #     raise Exception("{0} not exists", filename)

    def __del__(self):
        print(f"{self} over!!")
        self.fp.close()

    def checkLine(self, line):
        ret = IDX_MAIN
        if line.find("理想同学") == 0:
            ret = IDX_FREE_WAKE
            print(f"{line} 标记的不是 主唤醒词")
        return ret

    """
    @return 返回的唤醒词 ID，负数为 误唤醒
    """

    def findNext(self, timestamp):

        if self.lastStartIndex > timestamp:
            # print("处在不应唤醒 而 唤醒序列")
            return CODE_FAULT_WAKE

        if self.lastStartIndex == 0 and self.lastEndIndex > timestamp:
            self.repeatWakeWordIndex += 1
            # print("处在已经 被唤醒 而 继续唤醒序列")
            return CODE_REPEAT_WAKE

        if self.lastEndIndex > timestamp:
            # print("正确唤醒")
            self.lastStartIndex = 0
            return IDX_MAIN

        self.lastStartIndex = 0
        self.lastEndIndex = 0
        """9798-45817-./TESTSET2/0825_62_G0206_f_43_江苏/理想同学/G0206_f_43_0007_norm.wav-56446-81022-D0149_ID0149W0031_游戏"""
        while 1:
            line = self.fp.readline()
            # print(f"{timestamp}-->{line}")
            if not line:
                break
            # 读取相应的行数
            ## 正则表达 获取相应 的 索引 范围
            r = re.compile('(\d+)-(\d+).*')
            m = r.match(line)
            if m is not None:
                startIndex = int(m.group(1)) / 16
                endIndex = int(m.group(2)) / 16 + MISTAKE_TIME_MS
                if startIndex < timestamp < endIndex:
                    self.lastEndIndex = endIndex
                    return self.checkLine(line)
                elif startIndex > timestamp:
                    # print("处在不应唤醒 而 唤醒序列")
                    # 误唤醒
                    self.lastStartIndex = startIndex
                    self.lastEndIndex = endIndex
                    return CODE_FAULT_WAKE
                elif endIndex < timestamp:
                    # 应该唤醒 却没有唤醒
                    self.shouldWakeWordCount += 1
                    self.wakeWordTimeRange.append(startIndex)
                    continue
                else:
                    print(f"start {self.lastStartIndex}ms , end {self.lastEndIndex}ms,find {timestamp} ms")
                    return CODE_UNKNOWN
        return CODE_FILE_OVER

    def over(self):
        while 1:
            line = self.fp.readline()
            if not line:
                print("tag file check over!!!!")
                break
            # 读取相应的行数
            ## 正则表达 获取相应 的 索引 范围
            r = re.compile('(\d+)-(\d+).*')
            m = r.match(line)
            if m is not None:
                startIndex = m.group(1)
                self.shouldWakeWordCount += 1
                self.wakeWordTimeRange.append(int(startIndex) / 16)
        pass

    def sum(self):
        print("应该唤醒而未唤醒次数:{0}".format(self.shouldWakeWordCount))
        print("应该唤醒而未唤醒 起始 ms 分别是")
        for i in self.wakeWordTimeRange:
            print(i, end=",")
        print()
        pass


class LOG_WORDS:
    categoryOneShot = 0
    categoryNormal = 0

    def __init__(self, filename):
        # try:
        self.fp = open(filename, "r", encoding='UTF-8')
        # except:
        #     print("{0} not exists", filename)
        # pass

    def obtainWakeTimestamp(self):
        while 1:
            line = self.fp.readline()
            if not line:
                print("log file check over!!!!")
                break
            """2001-01-01 08:02:55.351 DEBUG mkws.cpp:265: [mkws] frame 0457,time 7.312,channel 1, word 00, score: 0.998047,threshold:0.600000, 2"""
            r = re.compile(
                '.*\[mkws\] frame (\d+),time (\d*.\d*),channel (\d+), word (\d+)')
            m = r.match(line)
            if m is not None:
                return float(m.group(2)) * 1000, int(m.group(3)), int(m.group(4)), None
            else:
                r1 = re.compile('.*channel=\d+,wordIndex=(\d+),type=\d+,category=(\d+)')
                m1 = r1.match(line)
                if m1 is not None:
                    categoryIndex = int(m1.group(2))
                    if categoryIndex == 0:
                        self.categoryNormal += 1
                    else:
                        self.categoryOneShot += 1
                else:
                    r2 = re.compile('.*start: \d+fileName: ([\s\S]+)')
                    m2 = r2.match(line)
                    if m2 is not None:
                        self.printCategory()
                        self.categoryNormal = 0
                        self.categoryOneShot = 0
                        return -1, -1, -1, str(m2.group(1)).strip()
                        pass
                    pass
        return -1, -1, -1, None

    def printCategory(self):
        print(f"普通唤醒:{self.categoryNormal}")
        print(f"oneshot :{self.categoryOneShot}")


class DataCollect:

    def __init__(self, filename):
        self.audioFile = filename
        self.wakeRightRange = []
        self.wakeFaultRange = []
        self.wakeRepeatRange = []
        self.wakeFreeWakeRange = []
        self.wakeRightCount = 0
        self.wakeFaultCount = 0
        self.wakeRepeatCount = 0
        # 不在标记区间内 并且是免唤醒词的 次数
        self.wakeFreeWakeCount = 0
        pass

    def addRight(self, timestamp):
        self.wakeRightCount += 1
        self.wakeRightRange.append(timestamp)

    def addFault(self, timestamp):
        self.wakeFaultCount += 1
        self.wakeFaultRange.append(timestamp)

    def addRepeat(self, timestamp):
        self.wakeRepeatCount += 1
        self.wakeRepeatRange.append(timestamp)
        pass

    def addFree(self, timestamp):
        self.wakeFreeWakeCount += 1
        self.wakeFreeWakeRange.append(timestamp)
        pass

    def printResult(self):
        print("=============================")
        print(f"=== {self.audioFile} , timestamp :{file_time_ms[self.audioFile]}")
        # print(f"总共触发 {count} 次唤醒")
        print("正确唤醒次数:{0}".format(self.wakeRightCount))
        print("误唤醒次数(包含免唤醒词落在标记区间内 以及 主唤醒词未落在标记区间内):{0}".format(self.wakeFaultCount))
        print("重复唤醒次数:{0}".format(self.wakeRepeatCount))

        print("正确唤醒 起始 ms 分别是")
        for i in self.wakeRightRange:
            print(i, end=',')
        print()
        print("误唤醒 起始 ms 分别是")
        for i in self.wakeFaultRange:
            print(i, end=',')
        print()
        print("重复唤醒 起始 ms 分别是")
        for i in self.wakeRepeatRange:
            print(i, end=',')
        print()
        print("=============================")


def main():
    """
    日志 与 tag 进行比对， 从而生成唤醒词的个数，误唤醒词等
    """
    # global tag
    # global dataCollect
    log = LOG_WORDS("log_m.elevoc.demo.txt")

    # 唤醒词 统计
    ## 日志中唤醒词 的获取 (需要打印 唤醒 所在的 位置 即帧数)
    # 误唤醒词 统计
    ## 获取所在位置
    # 应该唤醒 未唤醒 统计
    ## 逻辑处理
    ### 1. 相同 则 +1 2. 不同 ，不在同一区间则为 误唤醒，同一区间 不同唤醒词 也为 误唤醒 3. 应该 唤醒 没有 唤醒 也需要统计

    count = 0
    lastChannel = 0
    lastTimestamp = 0
    tag = None
    totalTimestamp = 0
    spanTimeStamp = 0
    dataCollect = None
    while 1:
        timestamp, channel, wordIndex, audioFile = log.obtainWakeTimestamp()
        # print(f"{timestamp}   --- {spanTimeStamp}")
        timestamp -= spanTimeStamp
        if audioFile is not None:
            if dataCollect is not None:
                dataCollect.printResult()
            dataCollect = DataCollect(audioFile[audioFile.rindex("/") + 1:])
            if tag is not None:
                tag.over()
                tag.sum()
                spanTimeStamp = totalTimestamp
            totalTimestamp += file_time_ms[audioFile[audioFile.rindex("/") + 1:]]

            # 找到 新的文件
            tag = TAG_WORDS("主唤醒词_tag.txt")
            continue
        if timestamp < 0:
            break

        count += 1
        tagIndex = tag.findNext(timestamp)
        if tagIndex == wordIndex:
            dataCollect.addRight(timestamp)
            lastChannel = channel
            lastTimestamp = timestamp
        elif tagIndex == CODE_REPEAT_WAKE:
            if wordIndex != 0:  # 免唤醒词
                dataCollect.addFault(timestamp)
                continue
            dataCollect.addRepeat(timestamp)
            # 需要增加为何重复唤醒 即 增加唤醒的 通道数
            print(f"此次重复唤醒 {channel, timestamp},上次是:{lastChannel, lastTimestamp}")
        elif tagIndex == CODE_FAULT_WAKE:
            # 这里需要区分 是 免唤醒词 还是 主唤醒词
            ## 如果是 免唤醒词 未 落在 tag标记的区间内 则 认为是 一种情况
            ## 如果是 免唤醒词 落在 tag标记的区间 内 则认为是 误唤醒词，计入误唤醒次数
            ## 如果是 主唤醒词 落在 非 tag标记的区间内 也认为 应当计入误唤醒词次数
            if wordIndex != 0:
                dataCollect.addFree(timestamp)
                continue
            dataCollect.addFault(timestamp)

    # tag.over()
    log.printCategory()
    dataCollect.printResult()
    tag.over()
    tag.sum()

    pass


if __name__ == '__main__':
    main()
