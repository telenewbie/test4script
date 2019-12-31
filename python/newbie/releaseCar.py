# encoding:utf-8
#    编译车机版本，需要改变字体大小以及需要增加签名文件
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
# <!--//车机字号：24 22 20 16 14 12-->
#     <!--后视镜字号：30 28 24 20 18 16-->
fontSize={"text_size_1":"@dimen/m12",
          "text_size_2":"@dimen/m14",
          "text_size_3":"@dimen/m16",
          "text_size_4":"@dimen/m20",
          "text_size_5":"@dimen/m22",
          "text_size_6":"@dimen/m24"}
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
print str
file = open(gradleFilepath, "wb")
file.write(str)
file.close()

file=open(dimenValues,"rb");
dimenStr="""
<resources>
<dimen name="text_size_1">@dimen/m12</dimen>
<dimen name="text_size_2">@dimen/m14</dimen>
<dimen name="text_size_3">@dimen/m16</dimen>
<dimen name="text_size_4">@dimen/m20</dimen>
<dimen name="text_size_5">@dimen/m22</dimen>
<dimen name="text_size_6">@dimen/m24</dimen>
""";
for line in file:
    if(line.strip().startswith('<dimen name="text_size_')):
        continue
    if (line.strip().startswith('<resources>')):
        continue
    dimenStr+=line
file.close()

file=open(dimenValues,"wb");
file.write(dimenStr)
file.close()

import os
os.chdir(projectPath)
os.system("gradle assembleCar")
file = open(gradleFilepath, "wb")
file.write(oldstr)
file.close()
