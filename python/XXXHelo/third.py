# coding:utf-8
CODEC = 'utf-8'
print '我是汉字'
# 写入文件
File = "test.txt"
content = u'hello world'
import codecs
content1 = u'你好，脚本之家 jb51.net'
ffff = codecs.open(File,'w','utf-8')  #可以写入中文到文件中
ffff.write(content1)
ffff.close()
print "采用codecs 的方式进行写中文",
fileContent = open(File,"r")
print fileContent.read()
fileContent.close()

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
fileContent = open(File,"wt")
fileContent.write(content1)
fileContent.close()

print "采用直接open 的方式进行写中文",
fileContent = open(File,"r")
print fileContent.read()
fileContent.close()
import io
with io.open(File,'w',encoding='utf-8') as f:
    f.write(unicode("\xEF\xBB\xBF", "utf-8"))#函数将\xEF\xBB\xBF写到文件开头，指示文件为UTF-8编码。
    f.write(content1)
print "采用io.open 的方式进行写中文",
with open(File,"r") as f:
    print f.read()

f = open(File, "a+")
f.write(content)
f.close()
del f
f = open(File, "r")
for eachline in f:
    print eachline
f.close()
# f = open(File, "r")
# bytes_in = f.read()
# print bytes_in.encode(CODEC)

# 查找字符串
import re

m = re.search('\\[rtfvn]', r"Hello world!\n")
if m is not None:
    print  m.group()
else:
    print 'not search'
m = re.search(r'\\n', r"Hello world!.\n")#注意匹配字符串和搜索字符串前的r的作用
if m is not None:
    print  m.group()
else:
    print 'not search'


# 列表解析
def testlie():
    lis = [i for i in range(10) if i % 2 == 0]
    print lis
    for i, t in enumerate(lis):
        print i, "==", t
testlie()
# 方法使用Map保存
# choice={"V":testlie} #此处不加（）不会执行方法体
# choice['V']() #此处会执行方法体

# 队列
stack=[]

tips = """
(E)nqueue
(D)equeue
(V)iew
(Q)uit

Enter choice
"""

####入队
def enqueue():
    stack.append(raw_input('input your New String'))
    pass

####出队
def dequeue():
    if len(stack)>0:
        print stack.pop() #这里是堆栈LIFO(后进先出)如果改成stack.pop(0),则为队列（FIFO）
    else:
        print "stack is empty"
    pass

####查看
def view():
    print stack
    pass


choiceMap = {'e': enqueue,'d':dequeue,'v':view,'q':''}
while True:
    try:
        choice = raw_input(tips).strip()[0].lower()  #strip的作用和java的trim的作用是一样的
    except:
        choice = 'q'
    print "you choice is ", choice
    if choice not in choiceMap:
        print 'invalid option,try again'
        continue
    if choice == 'q':
        break
    choiceMap[choice]()


