#coding:utf-8

import Levenshtein

labels = []
with open("label_asr.txt","r") as fl:
    for line in fl.readlines():
        labels.append(line.strip().split("\t")[1])

passIndex = []


# for label in labels:
score = Levenshtein.distance(labels[274], "关空调内外循环智能部门")
CharCount = len(labels[274])
CER = score / float(CharCount) if CharCount > 0 else 0

print(CER)