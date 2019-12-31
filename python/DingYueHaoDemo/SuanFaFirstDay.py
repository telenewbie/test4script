# encoding:utf-8


#
# 题目一:
# 简述：这里有四个数字，分别是：1、2、3、4
# 提问：能组成多少个互不相同且无重复数字的三位数？各是多少？

import Utils


# 解法一
# -----------------------------------------------------
def timu1():
    print "解法一"  # 时间复杂度相同,此种方式更耗时
    # data = [1, 2, 3, 4]
    startTime = Utils.getCurrentTimestamp()
    data = range(1, 5)
    for a in data:
        for b in [x for x in data if x != a]:
            for c in [x for x in data if x != a and x != b]:
                pass
                # print "%d_%d_%d" % (a, b, c)
                # for d in [x for x in data if x != a and x != b and x != c]:
                # print "%d_%d_%d_%d" % (a, b, c, d)
    print Utils.getCurrentTimestamp() - startTime


# -----------------------------------------------------
# 解法二
# -----------------------------------------------------
def timu1G():
    print "解法二"
    startTime = Utils.getCurrentTimestamp()
    for a in range(1, 5):
        for b in range(1, 5):
            for c in range(1, 5):
                if (a != b and b != c and a != c):
                    pass
                    # print a, b, c
    print Utils.getCurrentTimestamp() - startTime


# -----------------------------------------------------


# 题目二
#
# 简述：企业发放的奖金根据利润提成。利润(I)低于或等于10万元时，奖金可提10%；
# 利润高于10万元，低于20万元时，低于10万元的部分按10%提成，高于10万元的部分，可提成7.5%；
# 20万到40万之间时，高于20万元的部分，可提成5%；
# 40万到60万之间时高于40万元的部分，可提成3%；
# 60万到100万之间时，高于60万元的部分，可提成1.5%，
# 高于100万元时，超过100万元的部分按1%提成.
#
# 提问：从键盘输入当月利润I，求应发放奖金总数？


def timu2():
    # 解法一:自己写的.太差劲了
    sum = 0
    monkey = int(raw_input("当月所得利润"))
    if (monkey <= 10):
        sum = monkey * 1.1
    elif (20 > monkey > 10):
        sum = 11 + (monkey - 10) * 0.075
    return sum


def timu2G():
    i = int(raw_input('净利润:'))
    arr = [1000000, 600000, 400000, 200000, 100000, 0]
    rat = [0.01, 0.015, 0.03, 0.05, 0.075, 0.1]
    r = 0
    for idx in range(0, 6):
        if i > arr[idx]:
            r += (i - arr[idx]) * rat[idx]
            # print (i - arr[idx]) * rat[idx]
            i = arr[idx]
    return r


# 题目三
# 简述：一个整数，它加上100和加上268后都是一个完全平方数
#
# 提问：请问该数是多少？
def timu3():
    # 一开始不理解什么是:完全平方数,一个数的平方根的平方等于自身
    # 这道题做错了,第一:不知道这里要进行强转,第二不知道完全平方数
    import math
    result = []
    for x in range(1, 1000):
        i = math.sqrt(x + 100)  # 这里需要进行int()强转
        j = math.sqrt(x + 268)
        if (x + 100 == i * i) and (x + 268 == j * j):
            print "%f,%f,%f,%f,%f" % (x, i, i * i, j, j * j)
            result.insert(len(result), x)
    return result


def timu3G():
    import math
    result = []
    for i in range(10000):
        # 转化为整型值
        x = int(math.sqrt(i + 100))  # 这里需要强转,
        y = int(math.sqrt(i + 268))
        if (x * x == i + 100) and (y * y == i + 268):
            # print i
            result.insert(len(result), i)
    return result


# 题目四
# 简述：要求输入某年某月某日
# 提问：求判断输入日期是当年中的第几天？


def timu4():
    year = int(input("year"))
    month = int(input("month"))
    day = int(input("day"))
    # 判断是否是闰年
    # 判断所属月份是当年的第几个月份
    # 判断之前的月份天数相加+当前的天数

    pass


def timu4G():
    year = int(raw_input('year:\n'))
    month = int(raw_input('month:\n'))
    day = int(raw_input('day:\n'))

    months = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
    if 0 < month <= 12:
        sum = months[month - 1]
    else:
        print 'data error'
    sum += day
    leap = 0  # www.iplaypy.com
    if (year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0)):
        leap = 1
    if (leap == 1) and (month > 2):
        sum += 1
    print 'it is the %dth day.' % sum





def main():
    # print timu2G()
    # print timu3()
    # print timu3G()
    # print timu4()
    timu4G()


if __name__ == '__main__':
    main()
