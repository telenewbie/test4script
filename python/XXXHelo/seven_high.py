#coding:utf-8
#高级用法
#re 字符串查找与匹配，注意使用complie进行预编译，有利于性能
import re
pattern=re.compile("(\w){2}(\w){2}")
# result=re.findall(pattern,"a hello world bccc")
#print result
result=re.match(pattern,"ccdffff")
print result.groups()



str1=input("enter number")
# 输出相应的类型
print type(str1)
print type(str(str1))
a=str(str1).isdigit()
print a
print type(a)
if a:
    if a ==1:
        print 1
    print 'true'
