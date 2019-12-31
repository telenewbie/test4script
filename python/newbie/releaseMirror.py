# encoding:utf-8
# 获取build.gradle的内容
projectPath = r"C:\Users\ASUS User\.ssh\kaola_txz_project\Tongxinzhe_KaolaFM_Radio\TXZ_KL_Radio"
dimenValues=projectPath+r"\src\main\res\values\dimens.xml";
gradleFilepath = projectPath + r"\build.gradle"

signingConfigsStr="""
    signingConfigs {
            release {
                keyAlias 'androiddebugkey'
                keyPassword 'android'
                storeFile file('F:/workspace/java/android/txz/txz.keystore')
                storePassword 'android'
            }
    }
"""

releaseStr="""
signingConfig signingConfigs.release
"""

file = open(gradleFilepath, "r")
str = ""
oldstr=""
for line in file:
    str += (line )
    oldstr+=(line )
    if(line.strip()=="android {"):
        str+=signingConfigsStr
    elif(line.strip()=="release {"):
        str+=releaseStr
file.close()
file = open(gradleFilepath, "wb")
file.write(str)
file.close()


file=open(dimenValues,"rb");
dimenStr="""
<resources>
<dimen name="text_size_1">@dimen/m16</dimen>
<dimen name="text_size_2">@dimen/m18</dimen>
<dimen name="text_size_3">@dimen/m20</dimen>
<dimen name="text_size_4">@dimen/m24</dimen>
<dimen name="text_size_5">@dimen/m28</dimen>
<dimen name="text_size_6">@dimen/m30</dimen>
""";
for line in file:
    if(line.strip().startswith('<dimen name="text_size_')):
        continue
    if (line.strip().startswith('<resources>')):
        continue
    dimenStr+=line
file.close()


import os
os.chdir(projectPath)
os.system("gradle assembleMirror")
file = open(gradleFilepath, "wb")
file.write(oldstr)
file.close()
