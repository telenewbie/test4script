# encoding:utf-8
# python 算法题目

# 整数顺序排列问题简述：任意三个整数类型，x、y、z
# 提问：要求把这三个数，按照由小到大的顺序输出
data = [1, 3, 2, 5, 6, 4, 0]


def timu5():
    print data[0:-1]
    # 冒泡排序
    # for x in reversed(data[0:-1]):
    #     for()
    #     pass


    # 选择排序

    # 插入排序


    pass


def timu5G():
    print sorted(data)


# 要求一：输出第10个斐波那契数列,求和
# 要求二：问题的要求改为：需要输出指定个数的斐波那契数列，要怎么来解决呢？我们往下看。
def timu6():
    result = []
    result.append(0)
    result.append(1)
    for x in range(2, 10):
        result.append(result[x - 2] + result[x - 1])
    print result


def fib(n):
    a, b = 1, 1
    for x in range(n - 1):
        a, b = b, a + b  # 这里可以连等于
    return a


def fib1(n):
    if n == 1:
        return [1]
    if n == 2:
        return [1, 1]
    fibs = [1, 1]
    for i in range(2, n):
        fibs.append(fibs[-1] + fibs[-2])
    return fibs


def timu6G():
    print fib(10)
    print fib1(10)


# Python练习题问题如下：
# 提问：将一个列表的数据复制到另一个列表中。
#
# 请仔细看要求，这里要求的是复制数据到一个新的列表中。
def timu7G():
    x = [1, 2, 3]
    y = x[:]
    print y
    # 修改原数组
    x[1:3] = [100, 1]  # 切片;[startIndex:length),startIndex 从0 开始,length表示总长,不包括在内
    print "原数组:", x
    print "新数组:", y


# 简述：9*9乘法口诀表。
# 要求：逐项单位输出。例如1的一行，2的一行，以此类推。

def timu8():
    for i in range(1, 10):
        print
        for j in range(1, i + 1):
            print "%d*%d=%d\t" % (i, j, i * j),  # 不换行的关键,这里多了一个","


def timu8G():
    for x in range(1, 10):
        print
        for y in range(1, x + 1):
            print "%d*%d=%d" % (x, y, x * y),


# 要求：随便写一段代码，测试time.sleep（）方法效果学习。
import time


def timu9():
    print "start"
    time.sleep(1)
    print "end"


def timu9G():
    myD = {1: 'a', 2: 'b'}
    for key, value in dict.items(myD):  # 注意遍历map的时候,需要把它变成一个Iterator
        print key, value
        time.sleep(1)


# 简述：暂停一秒time.sleep()输出；并格式化当前时间。
def timu10():
    # 格式化当前时间
    print time.time()  # 时间戳
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 并格式化当前时间。
    pass


def timu10G():
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    # 暂停一秒
    time.sleep(1)

    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


# 简述：话说有一对可爱的兔子，出生后的第三个月开始，每一月都会生一对小兔子。
# 当小兔子长到第三个月后，也会每个月再生一对小小兔子.
#
# 问题：假设条件，兔子都不死的情况下，问每个月的兔子总数为多少？

def timu11():
    # 以对为单位
    # 没有思路
    pass


def timu11G():
    # Python解题思路分析：兔子的规律为数列1, 1, 2, 3, 5, 8, 13, 21....，
    # 好似斐那波契数列的感觉哦~
    a1 = 1
    b2 = 1
    for i in range(1, 21):
        print '%12ld %12ld' % (a1, b2),
        if (i % 3) == 0:
            print ''
        a1 = a1 + b2
        b2 = a1 + b2


# 简述：区间范围101-200
#
# 要求：判断这个区间内有多少个素数，并逐一输出。

def timu12():
    import math
    sum = 0
    for i in range(101, 201):  # 这里应该是201而不是200
        finish = 1
        for j in range(2, int(math.sqrt(i)) + 1):  # [start,end)
            if i % j == 0:
                finish = 0
                break
        if finish == 1:
            sum += 1
            print i
    print "total is ", sum


# Python练习题问题如下：
# 要求：打印输出所有的"水仙花数"。
# 什么是水仙花数？
# 百度一下：水仙花数是指一个 n 位正整数 ( n≥3 )，它的每个位上的数字的 n 次幂之和等于它本身。
# （例如：1^3 + 5^3+ 3^3 = 153）。

def getGeWeiShu(i):
    if i == 0:
        return -1
    return i % 10


def timu13():
    import math
    for i in range(1, 100):
        print i,
        result = i
        suju = []
        while getGeWeiShu(result) >= 0:
            if int(result / 10) == 0:
                print getGeWeiShu(result),
                suju.append(getGeWeiShu(result))
                break
            else:
                print getGeWeiShu(result),
                suju.append(getGeWeiShu(result))
                result = int(result / 10)
        print
        for j in range(1, math.sqrt(i) + 1):
            # 将suju中的数据进行遍历,然后幂操作
            pass
    pass


# Python练习题问题如下：
# 要求：将一个正整数分解质因数；例如您输入90，分解打印90=2*3*3*5。

def timu14():
    import math
    while (True):

        testData = raw_input("请输入一个数:")
        if not testData.isdigit():
            print "请输入整数!!"
            return
        testData = int(testData)
        finish = 0
        print testData, "=",
        while finish == 0:
            if testData < 2:
                print testData,
                break
            for i in xrange(2, testData + 1):
                if testData % i == 0:
                    print i,
                    testData /= i
                    if testData == 1:
                        finish = 1
                    else:
                        print "*",
                    break
                if testData - 1 == i:
                    finish = 1
        print


def timu14G():
    while (True):

        n = raw_input("请输入一个数:")

        print '{} = '.format(n),
        # if not isinstance(n, int) or n <= 0:
        #     print 'iplaypy.com请输入一个正确的数字 !'
        #     exit(0)
        if not n.isdigit():
            print "请输入整数!!"
            return
        n = int(n)
        if n in [1]:
            print '{}'.format(n)
        while n not in [1]:  # 循环保证递归
            for index in xrange(2, n + 1):
                if n % index == 0:
                    n /= index  # n 等于 n/index
                    if n == 1:
                        print index
                    else:  # index 一定是素数
                        print '{} *'.format(index),
                    break


# 要求：获取输入的内容，并利用条件运算符的嵌套方式来完成这道题。
# 学习成绩>=90分的同学用A表示，60-89分之间的用B表示，60分以下的用C表示。
def timu15():
    score = int(raw_input('input score:\n'))
    if score >= 90:
        grade = 'A'
    elif score >= 60:
        grade = 'B'
    else:
        grade = 'C'
    print grade


# 用python方法如何输出指定格式形式的日期？
# D/M/Y
# 05/01/1941
# 06/01/1941
# 05/01/1942
def timu16():
    import datetime
    print datetime.date.today().strftime("%d/%m/%Y")
    rdata = datetime.date(1941, 1, 5)
    print rdata.strftime("%d/%m/%Y")
    print (rdata + datetime.timedelta(days=1)).strftime("%d/%m/%Y")
    print rdata.replace(year=rdata.year + 1).strftime("%d/%m/%Y")


# 输入一行字符，分别统计出其中英文字母、空格、数字和其它字符的个数。
def timu17():
    dig = 0
    alp = 0
    space = 0
    other = 0
    content = raw_input("请输入一行字符\n")
    for c in content:
        if c.isdigit():
            dig += 1
        elif c.isalpha():
            alp += 1
        elif c.isspace():
            space += 1
        else:
            other += 1
    print "%d,%d,%d,%d" % (dig, alp, space, other)


# 求这样的一组数据和，s=a+aa+aaa+aaaa+aa...a的值，其中a是一个数字；
# 例如：2+22+222+2222+22222(此时共有5个数相加)，这里具体是由几个数相加，由键盘控制。

def timu18():
    count = raw_input("几个数相加\n")
    if not count.isdigit():
        print "请输入一个数字"
        return
    count = int(count)
    test = 0
    for i in range(count):
        result = ''
        for j in range(i, count):
            result += '2'
        print result,
        if i != count - 1:
            print "+",
        test += int(result)
    print "=", test

def timu18G():
    Tn = 0
    Sn = []
    n = int(raw_input('n = :\n'))
    a = int(raw_input('a = :\n'))
    for count in range(n):
        Tn = Tn + a
        a = a * 10
        Sn.append(Tn)
        print Tn

    Sn = reduce(lambda x, y: x + y, Sn)
    print Sn

def main():
    timu18G()

    # timu18()

    # timu17()

    # timu16()
    # timu15()
    # timu14()
    # timu14G()
    # timu13()
    # timu12()
    # timu11G()
    pass
    # timu10()
    # timu10G()
    # timu5()
    # timu5G()
    # timu6()
    # timu6G()
    # timu7G()
    # timu8()
    # timu8G()
    # timu9()
    # timu9G()


if __name__ == '__main__':
    main()
