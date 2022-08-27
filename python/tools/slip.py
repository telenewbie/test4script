# coding=utf8

import os
import re
import datetime

file_pattern = re.compile('frame_(\d+)_(\d+)_([\d\.])+_kws_\d_oneshot_\d_vad_ch_\d_\d+_\d+\.pcm')


def createDir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("create ", path)


def extraTargetChannelPcm(pcmFile, targetChannel):
    """将 6 通道的数据 提取出指定通道的数据 """
    targetFile = f"{pcmFile[:-4]}_ch{targetChannel}.pcm"

    inLen = os.stat(pcmFile).st_size
    with open(pcmFile, 'rb') as f:
        if pcmFile[-4:] == ".wav":
            f.seek(44)
            inLen = inLen - 44
        with open(targetFile, "wb") as fw:
            while inLen > 0:
                data = f.read(12)
                fw.write(data[targetChannel * 2:targetChannel * 2 + 2])
                inLen = inLen - 12
    return targetFile


def takeSecond(elem):
    return elem[0]


def calSlipTag(inDir):
    """
    统计切片的 tag
    """
    data = []
    for path, dirnames, filenames in os.walk(inDir, topdown=False):
        if path != inDir:
            continue
        for filename in filenames:
            match = file_pattern.match(filename)
            if not match or len(match.group()) != len(filename):
                continue
            else:
                startFrame = int(match.group(1).strip())
                startTime = int(match.group(3).strip())
                needFrame = int(match.group(2).strip())

                seekPos = (startFrame - 2) * 16 * 1 * 2 * 16
                # seekPos = startTime * 16 * 1 * 2
                writeLen = os.stat(path + "//" + match.group()).st_size
                data.append([seekPos, writeLen, match.group(0)])
    data.sort(key=takeSecond)
    outFilePath = f"label_vad.txt"
    with open(outFilePath, "w") as fw:
        for seekPos, writeLen, filename in data:
            fw.writelines(f"{seekPos}\t{writeLen}\t{filename}\n")
    return outFilePath


def slipPcm(slipTag, filePath, subdir):
    inDir = "."
    if '\\' in filePath:
        inDir = filePath[:filePath.rindex("\\")]
    elif "/" in filePath:
        inDir = filePath[:filePath.rindex("/")]

    createDir(f"{inDir}/{subdir}")
    data = []

    with open(slipTag, "r") as fl, open(filePath, 'rb') as f:
        for line in fl.readlines():
            lineRes = line.split("\t")
            seekPos = int(lineRes[0].strip())
            writeLen = int(lineRes[1].strip())
            filename = lineRes[2].strip()
            seekRet = f.seek(seekPos)
            if seekRet < 0:
                print(f"error !!! {filename} -- {seekPos}  -- {writeLen}")
            outFileName = '{0}/{1}/{2}.pcm'.format(inDir, subdir, filename[:-4])
            with open(outFileName, "wb") as fw:
                fw.write(f.read(writeLen))
                fw.flush()

    # with open(filePath, 'rb') as f:
    #     for path, dirnames, filenames in os.walk(inDir):
    #         subdirLen = len(subdir)
    #         if path[-1 * subdirLen:] == subdir:
    #             # print(dirnames)
    #             # print(path)
    #             # print(filenames)
    #             continue
    #         for filename in filenames:
    #             match = file_pattern.match(filename)
    #             if not match or len(match.group()) != len(filename):
    #                 continue
    #             else:
    #                 startFrame = int(match.group(1).strip())
    #                 startTime = int(match.group(3).strip())
    #                 needFrame = int(match.group(2).strip())
    #                 outFileName = '{0}/{1}/{2}.pcm'.format(path, subdir, filename[:-4])
    #                 with open(outFileName, "wb") as fw:
    #                     seekPos = (startFrame - 2) * 16 * 1 * 2 * 16
    #                     # seekPos = startTime * 16 * 1 * 2
    #                     writeLen = os.stat(path + "//" + match.group()).st_size
    #                     seekRet = f.seek(seekPos)
    #                     if seekPos < 0:
    #                         print(f"error !!! {outFileName} -- {seekPos}")
    #                     fw.write(f.read(writeLen))
    #                     fw.flush()
    #                     data.append(outFileName)
    return data


def preProcess():
    isNewbie = False
    print("""
*******************************
欢迎使用 NEWBIE工具 之 切 VAD V1.0.0
*******************************
    """
          )
    inFile = ""
    label_vad = "label_vad.txt"
    targetChannel = 0
    re_vad = ""
    if not isNewbie:
        while 1:
            inFile = input("请输入需要处理的文件:")
            folder = os.path.exists(inFile)
            if not folder:
                print("文件不存在，请检查路径")
                continue
            else:
                break
        re_vad = input("需要重新生成VAD时间戳吗[N]")

        targetChannel = int(input("请输入需要提取的目标通道:"))
    else:
        inFile = r"D:\tmp\test\elevoc5\output\native"

    now = datetime.datetime.now()
    date_time = now.strftime("%Y%m%d%H%M%S")
    inDir = "."
    if '\\' in inFile:
        inDir = inFile[:inFile.rindex("\\")]
    elif "/" in inFile:
        inDir = inFile[:inFile.rindex("/")]
    if not (re_vad == "" or re_vad == "N"):
        label_vad = calSlipTag(inDir)

    targetFile = extraTargetChannelPcm(inFile, targetChannel)
    # targetFile = r"D:\tmp\test\2022-08-19_13_13_17\ev_in_1_ch6_20210418224808148_ch3.pcm"
    subDir = f"slip_{date_time}"
    targetPath = f"{inDir}/{subDir}"
    slipPcm(label_vad, targetFile, f"{subDir}")
    return targetPath
