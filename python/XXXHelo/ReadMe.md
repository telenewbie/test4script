## first.py
1. 先决条件
    ```python
    # coding:utf-8 # 表明该文件的格式
    # main 函数
    if __name__ =="__main__":
        pass
    ```
1. 展示了最基本的python语法
    - tuple元组 `()` 表示不可更改内容的数组， 
    - list 列表 `[]` 表示集合可用`[]` 对元素进行访问，也可`insert`
    - dict 字典 `{Key:value}` 表示键值对的集合，类似java 的map
    - set `{}` 表示值唯一,无序的集合 ，类似java 的 `ArraySet`
2. 字符串的截取，反转等，可以通过 `[(startIndex):(endIndex):(step)]` eg:`[1:-1:-1]` 表示 从第一个到倒数第一个，按照倒序 1 的步长来执行
4. 表达式
   ```python
    # 创建一个偶数倍数的列表
    [x * 2 for x in range(4) if not x % 2]
    # 创建一个偶数倍数的元组
    (x * 2 for x in range(4) if not x % 2)
    ```
3. lambda
    ```python
    print set(map(lambda x: x if x % 2 else "", range(7)))
    ```
3. 其他
    ```python
    # 创建C语言的printf的形式
    print "%s is number %d" % ("python", 1)
    # 字符可以直接变成20个
    print '-' * 20
    # 使用","进行加,输出中间有空格的间隔
    print "~loop#",1   # 输出 “~loop# 1”
    ```
4. 异常
    ```python
    # python 2.x 的异常捕获的方式
    try:
        pass
    except ZeroDivisionError, e:
        pass
    
    # python 3.x 的异常捕获方式
    try:
        pass
    except ZeroDivisionError as e:
        pass
    ```
1. 类的声明
    ```python
    class MyFoo:
        def __init__(self, nm="Joe"):
            pass
        def showname(self):
            """这里写函数功能简介"""
            pass
    ```
## Second.py
[参考：str()、repr()的区别](https://blog.csdn.net/kongsuhongbaby/article/details/87398394)
1. 写文件的方式：
```python
content = open(file_name, "r")
for eachline in content: #注意这样可以便利内容
    print eachline
```
1. repr 和str 的区别

    1.除了字符串类型外，使用str还是repr转换没有什么区别，字符串类型的话，外层会多一对引号，这一特性有时候在eval操作时特别有用；
    
    2.命令行下直接输出对象调用的是对象的repr方法，print输出调用的是str方法
1. 内置函数
```python
print isinstance("test", str)  # 使用isInstance
# 强转
str()
tuple()
list()
dict()
#长度
len()
```
3. 导入内部库
```python
from types import StringType
if (type("test") == StringType):
    pass

import string
print string.upper("test")

from string import Template
s = Template('there are ${money} ${lang} symbols')  # 注意这里是${key}的形式
print s.substitute(lang=1, money="10000")  # 使用的方式是;key=value的形式
```

## third.py
[参考：中文写文件](https://www.cnblogs.com/baojun2014/p/9085533.html)
1. 写中文到文件
```python
File = "test.txt"
content1 = u'你好'
# 第一种方式：
import codecs
with codecs.open(File,'w','utf-8') as ffff:  #可以写入中文到文件中
    ffff.write(content1)
# 第二种方式
import io
with io.open(File,'w',encoding='utf-8') as f:
    f.write(unicode("\xEF\xBB\xBF", "utf-8"))#函数将\xEF\xBB\xBF写到文件开头，指示文件为UTF-8编码。
    f.write(content1)
#第三种方式：
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
with open(File,"wt") as fileContent:
    fileContent.write(content1)
```
2. 正则表达式
3. 神奇的写法
```python
def enqueue():
    pass
choiceMap = {'e': enqueue} # 这里可以放入函数的指针
choiceMap['e']() # 这里会调用方法
```
# 需要解决的问题
1. `''` `""` `""""""` 的区别？
2. 字符串前缀 `r` `u` 等等代表什么意思，还有哪些前缀？
[参考:字符串前缀u r b f](https://blog.csdn.net/tyttytzhz/article/details/85615648)