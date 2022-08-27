import os,sys
import pandas as pd
import Levenshtein,difflib



IN=os.path.join(sys.path[0],"OUT_CER - noise.xlsx")
OUT=os.path.join(sys.path[0],"OUT_CER_1.xlsx")


def levenshtein(str1, str2):
    totalError = 0
    replace=0
    delete=0
    insert=0
    hash_ErrorDetails={}
    s = Levenshtein.opcodes(str1, str2)
    #print(s)
    for tag, i1, i2, j1, j2 in s:
        if tag == 'replace':
            totalError += max(i2-i1, j2-j1)
            replace+=max(i2-i1, j2-j1)
            ErrorDetails=str1[i1:i2]+'->'+str2[j1:j2]
            if 'replace' not in hash_ErrorDetails:
                hash_ErrorDetails['replace']=[]
            hash_ErrorDetails['replace'].append(ErrorDetails)
        elif tag == 'insert':
            totalError += (j2-j1)
            insert+=(j2-j1)
            ErrorDetails=str2[j1:j2]
            if 'insert' not in hash_ErrorDetails:
                hash_ErrorDetails['insert']=[]
            hash_ErrorDetails['insert'].append(ErrorDetails)
        elif tag == 'delete':
            totalError += max(i2-i1, j2-j1)
            delete+=max(i2-i1, j2-j1)
            ErrorDetails=str1[i1:i2]
            if 'delete' not in hash_ErrorDetails:
                hash_ErrorDetails['delete']=[]
            hash_ErrorDetails['delete'].append(ErrorDetails)
    return delete,insert,replace,totalError,hash_ErrorDetails


def CERGroup(group):
    d = group['CER']
    w = group['CharCount']
    return (d * w).sum() / w.sum()

df=pd.read_excel(IN)

for index,row in df.iterrows():
    SER=1
    Text = str(df.loc[index,'Text']).strip()
    R_Text = str(df.loc[index,'Cloud_Text']).strip()
    CharCount=len(Text)
    if Text==R_Text:
        SER=0
    Seat=df.loc[index,'Seat']
    R_Seat=df.loc[index,'R_Seat']
    if Seat==R_Seat:
        Seat_YN=1
    else:
        Seat_YN=0
    Delete,Insert,Replace,totalError,hash_DISDetails=levenshtein(Text, R_Text)

    CER=totalError/float(CharCount) if CharCount>0 else 0
    df.loc[index,'CharCount']=CharCount
    df.loc[index,'SER']=SER
    df.loc[index,'CER']=CER
    df.loc[index,'Delete']=Delete
    df.loc[index,'Insert']=Insert
    df.loc[index,'Replace']=Replace
    df.loc[index,'DISDetails']=str(hash_DISDetails)
    df.loc[index,'Seat_YN']=Seat_YN

df.to_excel(OUT, sheet_name='TestCase', index=False)

# 根据分组计算平均值, CER为基于字数的加权平均
GroupedSeat = df.groupby('Seat')
CERBySeat_WeightMean = GroupedSeat.apply(CERGroup)

print('=================================================')
print('语音识别 字错误率CER')
print(CERBySeat_WeightMean)
print('=================================================')
