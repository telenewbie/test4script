# coding:utf-8

# 创建元祖
yuan = (1, 2, 3, 4)
# yuan[1]=0
print (yuan)
test = "你好"
print (test)
# 创建列表,java对应数组
xxx = [1, 2, 3, 4, 5, 6, 7, 8,9]
xxx[1] = 10
xxx.insert(0,111)
print xxx
print xxx[::-1]
print xxx[1:10:2]
# 创建set
set_lie = {1, 31, 4, 3, 3, 30}
# lie[1]=10
print set_lie
for i in set_lie:
    print i
set_lie.add(10)
print set_lie
# print set_lie[::-1]
# 创建MAP字典
lie = {"V": test, "M": "nihao"}
print lie.get("V");
print len(lie)
# 创建C语言的printf的形式
print "%s is number %d" % ("python", 1)
# name=raw_input('enter you name');
# print name
# help(raw_input)

# 字符串获取个数
var1 = "this is just test";
print var1[1]
# 大数字
print 1.1
print '-' * 20
# if条件语句
if test < 1:
    print '111'
elif test > 1:
    print("222")
else:
    print "333"
# while条件语句
count = 0
while count < 3:
    print "loop#%d" % count
    print "~loop#",count  # 使用","进行加,输出中间有空格的间隔
    count += 1
# for循环
for v in yuan:
    print "%s" % v
for yuanv in range(len(yuan)):
    print yuan[yuanv], "\t(%d)" % yuanv
squared = [x * 2 for x in range(4) if not x % 2] #x%2返回值为0表示为false,not 0 表示为true
for i in squared:
    print i
# 打开文件
var1 = open("xxx.txt", 'r')
if var1:
    for eachline in var1:
        print eachline #为什么会多了一行
    var1.close()
# 捕获异常
try:
    i == 1 / 0
    print i
except ZeroDivisionError, e:
    print "occur error"
    print e


# 函数
def addMe(x1):
    'add Me'
    return x1 + x1


print addMe(2)
print addMe([1, 3, 4, 5])


# 类
class MyFoo:
    def __init__(self, nm="Joe"):
        """constract构造函数"""
        self.name = nm
        print 'create a class instace for', nm

    def showname(self):
        """display name"""
        print "My name is:", self.__class__.__name__
        print "Your name is:", self.name
    pass

fool = MyFoo('tele')
fool.showname()

#导入模块
import  sys
sys.stderr.write("hello sys\n")
print sys.version,sys.copyright,sys.path,sys.platform
#多重赋值，多元赋值
x=y=z=1;
print x,"-"*10,y,"-"*10,z,"-"*10
x,y,z=1,2,3
print x,"-"*10,y,"-"*10,z,"-"*10
print set(map(lambda x: x if x % 2 else "", range(7)))

# bev=eval("%s_version")
# g = {'__builtins__':{}}
# bev=eval('abs(-1)',g)
print globals()
l=locals()
print l
print eval("x+1",{},l)
# print  "测试eval的表达式是什么意思:",type(bev)
if __name__ =="__main__":
    print "主程序"