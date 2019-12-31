# encoding:utf-8


# 什么是完数？
# 完全数，又被称作完美数或完备数，是一些特殊的自然数。
# 它所有的真因子（即除了自身以外的约数）的和（即因子函数），恰好等于它本身。如果一个数恰好等于它的因子之和，则称该数为“完全数”。
# 用python方法找出1000以内的所有完数，并输出。
def timu19():
    import math
    for i in range(1000):
        result = 0
        k = []
        # end = int(math.sqrt(i))
        for j in range(1, i):
            if i % j == 0:
                result += j
                k.append(j)
                # print i, j
            if j == i - 1 and result == i:
                for x in k:
                    print x,
                print i


def timu19G():
    from sys import stdout
    for j in range(2, 1001):
        k = []
        n = -1
        s = j
        for i in range(1, j):
            if j % i == 0:
                n += 1
                s -= i
                k.append(i)

        if s == 0:
            print j
            for i in range(n):
                stdout.write(' ')
                stdout.write(str(k[i]))
            print k[n]


# 问题简述：假设一支皮球从100米高度自由落下。条件，每次落地后反跳回原高度的一半后，再落下。
# 要求：算出这支皮球，在它在第10次落地时，共经过多少米？第10次反弹多高？

def timu20():
    distance = 100.0
    r = 100.0
    for i in range(10):
        r = r / 2
        distance += 2 * r
    print distance, r


def timu20G():
    Sn = 100.0
    Hn = Sn / 2

    for n in range(2, 11):
        Sn += 2 * Hn
        Hn /= 2

    print 'Total of road is %f' % Sn
    print 'The tenth is %f meter' % Hn


# 问题简述：一只小猴子吃桃子的问题。
# 话说，一只小猴子第一天摘下若干个桃子，并吃了一半。感觉到吃的还不瘾，于是又多吃了一个；
# 第二天早上，又将剩下的桃子吃掉一半，又多吃了一个。
# 以后每天早上,都吃了前一天剩下的一半零一个。
# 请问，到了第10天早上想再吃时，却发现只剩下一个桃子了。求第一天共摘了多少？

def timu21():
    # x/2-1
    result = 1
    for i in range(9):
        result = (result + 1) * 2

    print result

    pass


def timu21G():
    x2 = 1
    for day in range(9, 0, -1):  # 倒序
        x1 = (x2 + 1) * 2
        x2 = x1
    print x1


# 简述：已知有两支乒乓球队要进行比赛，每队各出三人；
# 甲队为a,b,c三人，乙队为x,y,z三人；
# 已抽签决定比赛名单。
#
# 问题：有人向队员打听比赛的名单。a说他不和x比，c说他不和x,z比，请编程序找出三队赛手的名单。

# 其实我感觉我的更好,我的更智能.增加一问:输出所有的可能性
def timu22():
    one = ['a', 'b', 'c']
    two = ['x', 'y', 'z']

    temp = {}
    # 算出a有多少种可能,b有多少种可能,然后再拼凑在一起
    NotFind = True
    # while NotFind:
    for i in one:
        count = 0
        test = []
        for j in two:
            if i == 'a' and j == 'x':
                # continue
                pass
            elif i == 'c' and (j == 'x' or j == 'z'):
                # continue
                pass
            else:
                count += 1
                test.append(j)

            if j == two[len(two) - 1]:
                temp[i] = test


                # if count == 1 and j == two[len(two) - 1]:
                #     print i, j
                #     one.remove(i)
                #     two.remove(j)
                #     pass
    # if len(one) <= 0 or len(two) <= 0:
    #     NotFind = False
    result = []
    for key in temp.keys():
        for value in temp[key]:
            if value not in result:
                result.append(value)
                break
                # print key, value

    print result
    print temp
    pass


def timu22G():
    for i in range(ord('x'), ord('z') + 1):
        for j in range(ord('x'), ord('z') + 1):
            if i != j:
                for k in range(ord('x'), ord('z') + 1):
                    if (i != k) and (j != k):
                        if (i != ord('x')) and (k != ord('x')) and (k != ord('z')):
                            print 'order is a -- %s\t b -- %s\tc--%s' % (chr(i), chr(j), chr(k))


# 是要根据已经给出的一个菱形图案，用python方法完成一样效果的输出。
#    *
#   ***
#  *****
# *******
#  *****
#   ***
#    *

def timu23():
    count = 10
    for i in range(4):
        for j in range(3 - i):
            print " ",
        for j in range(i * 2 + 1):
            print "*",
        print
    for i in range(3):
        for j in range(i + 1):
            print " ",
        for j in range(6 - (2 * i + 1)):
            print "*",
        print


def timu23G():
    from sys import stdout
    for i in range(4):
        for j in range(2 - i + 1):
            stdout.write(' ')
        for k in range(2 * i + 1):
            stdout.write('*')
        print

    for i in range(3):
        for j in range(i + 1):
            stdout.write(' ')
        for k in range(4 - 2 * i + 1):
            stdout.write('*')
        print


# 问题简述：有一分数序列：2/1，3/2，5/3，8/5，13/8，21/13
# 要求：求出这个数列的前20项之和。

def timu24():
    a = 2.0
    b = 1.0
    sum = 0.0
    for i in range(20):
        sum += a / b
        c = a
        a = a + b
        b = c
    print sum


def timu24G():
    a = 2.0
    b = 1.0
    s = 0.0
    for n in range(1, 21):
        s += a / b
        b, a = a, a + b
    print s


def timu24G1():
    a = 2.0
    b = 1.0
    l = []
    for n in range(1, 21):
        b, a = a, a + b
        l.append(a / b)
    print reduce(lambda x, y: x + y, l)


# 阶乘：也是数学里的一种术语；
# 阶乘指从1乘以2乘以3乘以4一直乘到所要求的数；
# 在表达阶乘时，就使用“！”来表示。如h阶乘，就表示为h!；
#
# Python练习题问题如下：
# 提问：求1+2!+3!+...+20!的和

def timu25():
    # 可以更加优化
    sum = 0
    for i in range(1, 21):
        a = 1
        for j in range(1, i + 1):
            a *= j
        sum += a
    print sum
    # pass
    n = 0
    s = 0
    t = 1
    for n in range(1, 21):
        t *= n
        s += t
    print '1! + 2! + 3! + ... + 20! = %d' % s


def timu25G():
    s = 0
    l = range(1, 21)

    def op(x):
        r = 1
        for i in range(1, x + 1):
            r *= i
        return r

    s = sum(map(op, l))
    print '1! + 2! + 3! + ... + 20! = %d' % s


# Python练习题问题如下：
# 问题：要求用递归的方法，求5!阶乘
def timu26(x):
    if x == 0:
        return 0
    if x == 1:
        return 1
    else:
        return x * timu26(x - 1)


def test():
    for i in range(10):
        print "%d! = %d" % (i, timu26(i))


# Python练习题问题如下：
# 问题：要求利用递归函数调用的方式，将获取到所输入的5个字符，以相反顺序分别输出来。

def timu27(a):
    for i in range(len(a)):
        print a[len(a) - 1 - i]

    pass


def timu27G():
    def output(s, l):
        if l == 0:
            return
        print (s[l - 1])
        output(s, l - 1)

    s = raw_input('Input a string:')
    l = len(s)
    output(s, l)


# Python回推与递推的练习题如下：
# 问题描述：
# 已知有五位朋友在一起。第五位朋友他说自己比第4个人大2岁；
# 问第4个人岁数，他说比第3个人大2岁；
# 问第三个人，又说比第2人大两岁；
# 问第2个人，说比第一个人大两岁；
# 最后问第一个人，他说是10岁。
#
# 要求：求第5个人的年龄是多少。


# i 表示第几个人
def timu28(i):
    if i == 0:
        return 10
    else:
        return timu28(i - 1) + 2


# raw_input获取给定的一个不多于5位的正整数。
#
# 要求有二：
# 一、求它是几位数；
# 二、逆序打印出各位数字。

def timu29():
    s = raw_input("给定的一个不多于5位的正整数\n")
    if not s.isdigit():
        print "给定的一个不多于5位的正整数!!!!"
        return
    print "位数是:%d" % len(s)
    for i in range(len(s)):
        print s[len(s) - 1 - i]
    pass


# 问题描述：一个5位数，判断它是不是回文数。
def timu30():
    a = '1234321'
    # a = raw_input("回文数")

    b = []
    for i in range(len(a)):
        b.append(a[len(a) - 1 - i])
    if list(a) == b:
        print "ok"
    print b

    pass


# 获取输入内容，能过获取信息中星期几的第一个字母来判断一下是星期几。如果第一个字母一样，则继续判断第二个字母。
def timu31():
    days = {"M": "Monday", "Tu": "Tuesday", "W": "Wednesday", "Th": "Thursday", "F": "Friday", "Sa": "Saturday",
            "Su": "Sunday"}

    a = raw_input("请输入第一个字母")
    if a == 'T':
        a += raw_input("请输入第二个字母")
        if a == "Tu" or a == "Th":
            print days[a]
        else:
            print "error"

    pass


def timu31G():
    letter = raw_input("please input:")
    # while letter  != 'Y':
    if letter == 'S':
        print ('please input second letter:')
        letter = raw_input("please input:")
        if letter == 'a':
            print ('Saturday')
        elif letter == 'u':
            print ('Sunday')
        else:
            print ('data error')

    elif letter == 'F':
        print ('Friday')

    elif letter == 'M':
        print ('Monday')

    elif letter == 'T':
        print ('please input second letter')
        letter = raw_input("please input:")

        if letter == 'u':
            print ('Tuesday')
        elif letter == 'h':
            print ('Thursday')
        else:
            print ('data error')

    elif letter == 'W':
        print ('Wednesday')
    else:
        print ('data error')


# 按相反的顺序输出列表中的每一位值。
def timu32():
    a = ['one', 'two', 'three']
    for i in range(len(a)):
        print (a[len(a) - 1 - i])


def timu32G():
    a = ['one', 'two', 'three']
    for i in a[::-1]:
        print i


# 逗号分割列表。
def timu33():
    a = ['one', 'two', 'three']
    str = ""
    for i in a:
        str += i
        if i != a[len(a) - 1]:
            str += ","
    print str


def timu33G():
    L = [1, 2, 3, 4, 5]
    s1 = ','.join(str(n) for n in L)
    print s1


# Python设置文本文字颜色,此练习题需要用到Python class
def timu35():
    pass


def timu35G():
    class bcolors:
        HEADER = '\033[95m'

        OKBLUE = '\033[94m'

        OKGREEN = '\033[92m'

        WARNING = '\033[93m'

        FAIL = '\033[91m'

        ENDC = '\033[0m'

        BOLD = '\033[1m'

        UNDERLINE = '\033[4m'

    print bcolors.WARNING + "www.iplaypy.com 提示：此时文字颜色为浅黄色" + bcolors.ENDC

    class Logger:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'

    print Logger.OKBLUE + "info" + Logger.ENDC
    print Logger.HEADER + "info" + Logger.ENDC
    print Logger.WARNING + "info" + Logger.ENDC


# Python区间素数输出
def timu36(x, y):
    import math
    for i in range(x, y):
        # end = int(math.sqrt(i))
        find = False
        for j in range(2, i):
            if i % j == 0:
                # print i, j
                find = True
                break
                # print i, "%", j, (i % j)
        else:
            print i


def timu36G():
    lower = int(input("www.iplaypy.com 请您输入区间最小值: "))
    upper = int(input("www.iplaypy.com 请您输入区间最大值: "))
    for num in range(lower, upper + 1):
        # 素数大于 1
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                print(num)


# Python对input获取到的数据进行排序
def timu37():
    datas = []
    # for i in range(5):
    #     data = input("请输入第" + str(i) + "个数字")
    #     datas.append(int(data))
    datas = [9, 1, 8, 2, 6, 1, 0]
    # 冒泡排序
    # 快速排序
    for i in range(len(datas)):
        min = i
        for j in range(i + 1, len(datas)):
            if datas[min] > datas[j]:
                min = j
        datas[i], datas[min] = datas[min], datas[i]
    print datas


# Python练习题问题如下：
# 求一个3*3矩阵对角线元素之和

def timu38():
    # 多维数组
    datas = [
        [1, 2, 3],
        [4, 5, 6],
        [10, 8, 9]
    ]
    sum1 = 0
    for x, y in zip(range(3), range(2, -1, -1)):
        sum1 += datas[x][y]
    print sum1

    sum = 0
    for i in range(3):
        sum += datas[i][i]
    print sum


def timu38G():
    a = []
    sum = 0.0
    for i in range(3):
        a.append([])
        for j in range(3):
            a[i].append(float(raw_input("input num:\n")))
    for i in range(3):
        sum += a[i][i]
    print sum
    pass


# 已知有一个已经排好序的数组。要求是，有一个新数据项，要求按原来的规律将它插入数组中。

def timu39():
    a = [0, 1, 1, 2, 6, 8, 9]  # 排序规则为从小到大
    b = [7, 2, 3, 4, 10, 29]  # 乱序
    c = a + b
    # 快排
    for i in range(len(c)):
        min = i
        for j in range(i + 1, len(c)):
            if c[min] > c[j]: min = j
        c[min], c[i] = c[i], c[min]
    print c


# 已知数组python列表a = [99,66,25,10,3]，并且是已经排序过的。现在要求，将a数组的元素逆向排序。
def timu40():
    a = [99, 66, 25, 10, 3]

    sorted(a, lambda x, y: x > y)
    print a
    # for i in a[::-1]:
    #     print i


def main():
    timu40()
    # timu39()
    # timu38()
    # timu37()
    # timu36G()
    # timu36(0, 100)
    # timu35G()
    # timu33()
    # timu33G()
    # timu32()
    # timu32G()
    # timu31()
    # timu31G()
    # timu30()
    # timu29()
    # timu27([2, 3, 4, 5, 6])
    # print timu28(4)
    # timu27G()
    # test()
    # timu25()
    # timu25G()

    # timu24()
    # timu24G()
    # timu24G1()
    # timu23()
    # timu23G()
    # timu22()
    # timu22G()
    # timu21G()
    # timu21()
    # timu20G()
    # timu20()
    # timu19()
    # timu19G()


if __name__ == '__main__':
    main()
