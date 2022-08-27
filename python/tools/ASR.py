#!/usr/bin/env python
# coding=utf-8

import sys, os, codecs
import time
import json
import asyncio
import websockets
from uuid import uuid4
import base64
import hmac
from hashlib import sha1
import sys
import Levenshtein
import pandas as pd
from datetime import datetime
import re
from slip import preProcess

file_pattern = re.compile('frame_(\d+)_(\d+)_([\d\.])+_kws_\d_oneshot_\d_vad_ch_(\d)_\d+_\d+\.pcm')


def get_hmacsha1(key, data, sha1):
    hmac_code = hmac.new(bytes(key, encoding="utf-8"), bytes(data, encoding="utf-8"), sha1)
    return hmac_code.hexdigest()


async def audioRequest(ws, WavePath):
    content = {
        "aiType": "asr",
        "topic": "recorder.stream.start",
        "recordId": uuid4().hex,
        "audio": {
            "audioType": "pcm",
            "sampleRate": 16000,
            "channel": 1,
            "sampleBytes": 2
        },
        "asrParams": {
            # "customWakeupScore": -12,
            # "enableConfidence": False,
            # "enableNluRec": True,
            "enableNumberConvert": True,
            # "enablePunctuation": False,
            # "enableRecUppercase": False,
            # "enableTone": False,
            "enableVAD": False,
            "realBack": True,
            "vadPauseTime": 1000
        },
    }
    ASRText = ''
    recordId = ''
    Json = ''
    try:
        await ws.send(json.dumps(content))
        with open(WavePath, 'rb') as f:
            while True:
                chunk = f.read(3200)
                if not chunk:
                    await ws.send(bytes("", encoding="utf-8"))
                    break
                await ws.send(chunk)
        async for message in ws:
            resp = json.loads(message)
            if 'text' in resp:
                ASRText = ASRText + resp['text']
                recordId = recordId + '//' + resp['recordId']
                Json = Json + '//' + str(resp)
            if "eof" in resp and resp['eof'] == 1:
                break
    except websockets.exceptions.ConnectionClosed as exp:
        ws.close()
    return ASRText, recordId, Json


async def AISpeech_ASR(url, WavePath):
    async with websockets.connect(url) as websocket:
        time1 = time.time()
        ASRText, recordId, Json = await audioRequest(websocket, WavePath)
        time2 = time.time()
        responseTime = (time2 - time1) * 1000
    return ASRText, responseTime, recordId, Json


def wav_2_text(wav_path):
    if not os.path.exists(wav_path):
        raise RuntimeError(f'{wav_path} is not exists.')
    alias = '3.3_x_test'  # M分支为2.2test
    # productId = '279596921' #填入产品Id
    # deviceSecret = 'e7cec4d920a7487dbe198974f7ce0c86'
    # deviceName = 'BACK_f9dc66ef-d25b-40ed-b06b-0e43f0e0b900'

    productId = '279608551'  # 填入产品Id peiyu0623newforhaixia
    deviceSecret = '72be10467fb4467eb10c6d5f3b6d2d47'
    deviceName = 'virtual_X01_houhaixia'
    nonce = uuid4().hex
    tamp = str(int(time.time() * 1000))
    data = deviceName + nonce + productId + tamp
    sig = get_hmacsha1(deviceSecret, data, sha1)
    communicationType = "fullDuplex"
    url = f"wss://dds.dui.ai/dds/v3/{alias}?serviceType=websocket&productId={productId}&deviceName={deviceName}&nonce={nonce}&sig={sig}&timestamp={tamp}&communicationType={communicationType}"
    ASRText, responseTime, recordId, Json = asyncio.get_event_loop().run_until_complete(
        AISpeech_ASR(url, wav_path))
    return ASRText


def getTestData(dirpath):
    data = []
    for path, dirnames, filenames in os.walk(dirpath):
        if path != dirpath:
            continue
        for filename in filenames:
            match = file_pattern.match(filename)
            if not match or len(match.group()) != len(filename):
                continue
            else:
                channel = int(match.group(4).strip())
                # if filename[-4:] == ".pcm" and "oneshot" in filename:
                data.append([os.path.join(path, filename), channel])
    return data


# def convertPcm2Wav(dirpath,subdir):
#     data = []
#     for path, dirnames, filenames in os.walk(dirpath):
#         for filename in filenames:
#             if filename[-4:] == ".pcm" and filename[0:5] =="frame" and "oneshot" in filename:
#                 os.system("ffmpeg  -ar 16000 -ac 1 -acodec pcm_s16le -y -f s16le -i {0} {1}.wav > nul 2>nul".format(path+"\\"+filename,path+"\\"+subdir+"\\"+filename[:-4]))
#                 data.append(os.path.join(path, filename))
#                 sys.stdout.write(".")
#                 sys.stdout.flush()
#     print("")
#     return data

def takeSecond(elem):
    return elem[0][-21:]


def createDir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("create ", path)


def readLabels():
    labels = []
    with open("label_asr.txt", "r", encoding="utf-8") as fl:
        for line in fl.readlines():
            labels.append(line.strip().split("\t")[1])
    return labels


def CERGroup(group):
    d = group['CER']
    w = group['CharCount']
    return (d * w).sum() / w.sum()


isNewbie = False

if __name__ == "__main__":
    print("""
*******************************
欢迎使用 NEWBIE工具 之 ASR 版 V1.4.1

注意事项:
1. 需要把标签文件 label_asr.txt 放置到与本脚本相同目录下
2. 输出文件为excel ”asr_时间戳.xlsx“
3. 统计字错率是 SUM(CER*CharCount)/SUM(CharCount)
*******************************
    """
          )
    justAsr = input("是对 SDK 输出的数据 进行 ASR仿真吗？[Y]")
    dirpath = ""
    if justAsr == "Y" or justAsr == "":
        dirpath = ""
    else:
        dirpath = preProcess()

    if dirpath == "":
        # dirpath = ""
        if not isNewbie:
            while 1:
                dirpath = input("请输入需要处理的文件夹路径:")
                folder = os.path.exists(dirpath)
                if not folder:
                    print("文件夹不存在，请检查路径")
                    continue
                else:
                    break
        else:
            dirpath = r"D:\tmp\test\elevoc5\output\native"

    data = getTestData(dirpath)
    data.sort(key=takeSecond)
    labels = readLabels()
    i = 0
    lines = []
    for wav_data in data:
        outRes = wav_2_text(wav_data[0]).strip()
        # if outRes == "理想同学":
        #     continue
        label = labels[i] if i < len(labels) else ""
        score = Levenshtein.distance(label, outRes)
        CharCount = len(label)
        CER = score / float(CharCount) if CharCount > 0 else 0
        print(f"{i},{wav_data[1]},{label},{outRes},{CER},{CharCount},{wav_data[0]}")
        lines.append([i, wav_data[1], label, outRes, CER, CharCount, wav_data[0]])
        i = i + 1

        # if i == 20:
        #     break

    now = datetime.now()
    date_time = now.strftime("%Y%m%d%H%M%S")
    name = f"asr_{date_time}.xlsx"
    df = pd.DataFrame(data=lines, columns=["index", "channel", " label ", "cloud txt", "CER", "CharCount", "wav path "])
    df.to_excel(name, sheet_name="result")

    GroupedSeat = df.groupby('channel')
    CERBySeat_WeightMean = GroupedSeat.apply(CERGroup)
    print('=================================================')
    print('语音识别 字错误率CER')
    print(CERBySeat_WeightMean)
    print('=================================================')
