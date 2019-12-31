# coding:utf-8
import os


# file_name = raw_input("begin\n")
def test():
    while True:
        file_name = raw_input("enter your file name or enter to break\n")
        if (len(file_name) == 0):
            break
        if os.path.exists(file_name): #注意这里判断是否文件存在调用的是这个方法os.path.exists()
            content = open(file_name, "r")
            for eachline in content: #注意这样可以便利内容
                print eachline
        else:
            print 'this file is not exit'


test = "13aB"
test1 = "12"
print cmp(test1, test)
repr(test)
str(test)
print type(test)
print type('test')
print type("test")
print isinstance(test, str)  # 使用isInstance
from types import StringType  # 类似java的import java.String 和import java.String.TAG

if (type(test) == StringType):
    print "形同".decode(encoding='utf-8')
print repr(list(test))
print str(tuple(test))
print set(test)


# print dict(test) #强转
# 成员操作符
def testInAndNotIn():
    myinput = raw_input("input your Identifier")
    if len(myinput) > 1:
        if myinput[0] not in test:
            print """hello /t world"""
        else:
            for char in myinput[1:]:
                print char


import string
print string.upper(test)
# 字符串模板
from string import Template

s = Template('there are ${money} ${lang} symbols')  # 注意这里是${key}的形式
print "\rhaha"
print s.substitute(lang=1, money="10000")  # 使用的方式是;key=value的形式
#"""三引号的作用可以分行书写，会使转义字符转义，如果不需要转义则前面加r
print """print\r
test    good
1   one
2   two
3\tthree
<FrameLayout
        android:id="@+id/first_tab_container"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />
"""

