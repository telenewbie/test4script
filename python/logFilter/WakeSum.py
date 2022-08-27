# -*- coding: utf-8 -*-
import re

"""
统计 一段时间 内 与 标记文件 的对比, 从而得出 哪个 准确的唤醒率（包含 未唤醒的 时间戳等）
"""

CODE_FILE_OVER = -100
CODE_FAULT_WAKE = -1
CODE_REPEAT_WAKE = -2
CODE_UNKNOWN = -3
MISTAKE_TIME_MS = 300

# 主唤醒词 ID
IDX_MAIN = 0
# 免唤醒词 非0
IDX_FREE_WAKE = 100

## 文件的时间长度 ms
file_time_ms = {
    "aec_wakeup-asr.pcm": 3767735,
    "aec_w-wakeup-asr.pcm": 3744573,
    "quiet_L1_wakeup_asr.pcm": 342990,
}


class TagFile:
    def __init__(self, filename):
        self.fp = open(filename, "r", encoding='UTF-8')
        self.fp.seek(0)
        self.wakeWordTimeRange = []
        self.lastStartIndex = 0
        self.lastEndIndex = 0

    def __del__(self):
        self.fp.close()

    def checkLine(self, line):
        ret = IDX_MAIN
        if line.find("理想同学") == 0:
            ret = IDX_FREE_WAKE
            print(f"{line} 标记的不是 主唤醒词")
        return ret

    def findNext(self, timestamp):
        """
        @return 返回的唤醒词 ID，负数为 误唤醒
        """
        if self.lastStartIndex > timestamp:
            return CODE_FAULT_WAKE

        if self.lastStartIndex == 0 and self.lastEndIndex > timestamp:
            return CODE_REPEAT_WAKE

        if self.lastEndIndex > timestamp:
            self.lastStartIndex = 0
            return IDX_MAIN

        self.lastStartIndex = 0
        self.lastEndIndex = 0
        """9798-45817-./TESTSET2/0825_62_G0206_f_43_江苏/理想同学/G0206_f_43_0007_norm.wav-56446-81022-D0149_ID0149W0031_游戏"""
        while 1:
            line = self.fp.readline()
            if not line:
                break
            index = line.index("-")
            startIndex = int(line[0:index]) / 16
            str2 = line[index + 1:]
            endIndex = int(str2[0:str2.index("-")]) / 16 + MISTAKE_TIME_MS

            if startIndex < timestamp < endIndex:
                self.lastEndIndex = endIndex
                return self.checkLine(line)
            elif startIndex > timestamp:
                self.lastStartIndex = startIndex
                self.lastEndIndex = endIndex
                return CODE_FAULT_WAKE
            elif endIndex < timestamp:
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
                break
            index = line.index("-")
            startIndex = int(line[0:index]) / 16
            self.wakeWordTimeRange.append(startIndex)
        pass

    def getShouldWakeRange(self):
        return self.wakeWordTimeRange


class AudioFile:
    """
    音频文件 对应 的日志
    """

    def __init__(self, filename):
        self.filename = filename
        self.channel = -1
        self.timestamp = 0.0
        self.wordID = -1
        self.category = -1

    def parse(self, line):
        if "channel" not in line:
            return False
        self.timestamp, self.channel, self.wordID = self.countWakeupNum(line)
        if self.timestamp > 0:
            return True
        self.category = self.countCategory(line)
        if self.category >= 0:
            return True
        return False

    def countWakeupNum(self, line):
        """
        2001-01-01 08:02:55.351 DEBUG mkws.cpp:265: [mkws] frame 0457,time 7.312,channel 1, word 00, score: 0.998047,threshold:0.600000, 2
        @return  时间戳（ms） 通道数  以及 wordID
        """
        r = re.compile(
            r'.*\[mkws\] frame (\d+),time (\d*.\d*),channel (\d+), word (\d+)')
        m = r.match(line)
        if m is not None:
            return float(m.group(2)) * 1000, int(m.group(3)), int(m.group(4))
        return -1, -1, -1

    def countCategory(self, line):
        r = re.compile('.*channel=\d+,wordIndex=(\d+),type=\d+,category=(\d+)')
        m = r.match(line)
        if m is not None:
            return int(m.group(2))
        return -1


class Sum:
    def __init__(self, name):
        self.audioName = name
        self.wakeRightRange = {}
        self.wakeFaultRange = {}  # wordId
        self.wakeMisJudge = []
        self.wakeRepeatRange = {}
        self.shouldWake = []
        self.category = [0, 0, 0]

    def appendRightFlag(self, wordId, timestamp):
        if wordId not in self.wakeRightRange:
            self.wakeRightRange[wordId] = []
        self.wakeRightRange[wordId].append(timestamp)

    def appendRepeatFlag(self, channel, timestamp):
        if channel not in self.wakeRepeatRange:
            self.wakeRepeatRange[channel] = []
        self.wakeRepeatRange[channel].append(timestamp)

    def appendMisWakeFlag(self, wordId, timestamp):
        if wordId not in self.wakeFaultRange:
            self.wakeFaultRange[wordId] = []
        self.wakeFaultRange[wordId].append(timestamp)

    def __str__(self):
        detail = ""
        result = ""

        scoreCount = 0
        tmpScore = ""
        for key in self.wakeRightRange:
            value = self.wakeRightRange[key]
            if len(value) > 0:
                scoreCount += len(value)
                tmpScore = f"\nID[{key}]:"
                for v in value:
                    tmpScore += f"{v},"
        if scoreCount > 0:
            result += f"总共唤醒:{scoreCount} 次\n"
            detail += f"唤醒详情:{tmpScore}\n"

        wakeFaultCount = len(self.wakeFaultRange[0])
        if wakeFaultCount > 0:
            detail += "误唤醒 详情:\n"
            for value in self.wakeFaultRange[0]:
                detail += f"{value},"

        wakeMisJudge = len(self.wakeMisJudge)
        if wakeMisJudge > 0:
            detail += "误判 详情:\n"
            for value in self.wakeMisJudge:
                detail += f"{value},"
        if wakeFaultCount > 0 or wakeMisJudge > 0:
            result += f"误唤醒次数:{wakeMisJudge + wakeFaultCount}次"
            if wakeMisJudge > 0:
                result += f",其中误判 {wakeMisJudge} 次"
            result += "\n"
        wakeRepeatCount = 0
        tmp = "\n重复唤醒 详情:\n"
        tmp1 = ""
        for key in self.wakeRepeatRange:
            if len(self.wakeRepeatRange[key]) > 0:
                wakeRepeatCount += len(self.wakeRepeatRange[key])
                tmp1 += f"ch{key}:{len(self.wakeRepeatRange[key])},"
                tmp += f"ch{key}:"
                for value in self.wakeRepeatRange[key]:
                    tmp += f"{value},"
        if wakeRepeatCount > 0:
            result += f"重复唤醒:{wakeRepeatCount}次({tmp1})\n"
            detail += tmp

        tmp = ""
        for i, value in enumerate(self.category):
            if value > 0:
                tmp += f"cgy{i}:{value},"
        result += f"一共唤醒了{scoreCount + wakeFaultCount + wakeRepeatCount}次，类别:{tmp}\n"

        shouldWakeCount = len(self.shouldWake)
        if shouldWakeCount > 0:
            result += f"未唤醒词个数:{shouldWakeCount}\n"
            detail += "\n未唤醒词 详情:\n"
            for value in self.shouldWake:
                detail += f"{value},"

        result += "\n"

        return f"==============={self.audioName}=============\n" \
               f"{result}\n" \
               f"{detail}\n" \
               f"============================================\n"


def execute():
    f = None
    tag = None
    audio = None
    mySum = None
    listSum = []  # list
    spanTimeStamp = 0
    totalTimestamp = 0
    try:
        f = open("log_m.elevoc.demo.txt", "r", encoding='UTF-8')

        for line in f.readlines():
            content = line.strip()
            if "fileName:" in content:
                r = re.compile('.*start: \d+fileName: ([\s\S]+)')
                m = r.match(line)
                if m is not None:
                    if tag is not None:
                        tag.over()
                        mySum.shouldWake = tag.getShouldWakeRange()
                        spanTimeStamp = totalTimestamp

                    tag = TagFile("主唤醒词_tag.txt")
                    audioFileName = m.group(1)
                    name = audioFileName[audioFileName.rindex("/") + 1:].strip()
                    mySum = Sum(name)
                    audio = AudioFile(name)
                    listSum.append(mySum)
                    totalTimestamp += file_time_ms[name]

            elif audio is not None:
                # 解析
                if audio.parse(content):
                    if audio.timestamp > 0:
                        audio.timestamp -= spanTimeStamp
                        # 判断 该时间戳 是否 在 指定的范围内
                        retCode = tag.findNext(audio.timestamp)
                        # print(audio.timestamp, audio.channel, audio.wordID)
                        # print(f"retcode = {retCode}")
                        if retCode >= 0:  # 表明正确返回ID
                            if audio.wordID == retCode:
                                mySum.appendRightFlag(audio.wordID, audio.timestamp)
                            else:
                                print(f"--->{line}")
                                mySum.wakeMisJudge.append(audio.timestamp)
                        elif retCode == CODE_REPEAT_WAKE:
                            mySum.appendRepeatFlag(audio.channel, audio.timestamp)
                        elif retCode == CODE_FAULT_WAKE or retCode == CODE_FILE_OVER:
                            mySum.appendMisWakeFlag(audio.wordID, audio.timestamp)
                        elif retCode == CODE_UNKNOWN:
                            print(f"发生未知错误:timestamp={audio.timestamp}")
                        pass
                    elif audio.category >= 0:
                        mySum.category[audio.category] += 1
                else:
                    pass

    finally:
        if f is not None:
            f.close()
    if tag is not None and mySum is not None:
        tag.over()
        mySum.shouldWake = tag.getShouldWakeRange()
    for x in listSum:
        print(x)


if __name__ == '__main__':
    execute()
