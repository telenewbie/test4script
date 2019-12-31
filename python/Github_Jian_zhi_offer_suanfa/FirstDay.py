# encoding:utf-8
# 题目描述
# 在一个长度为 n 的数组里的所有数字都在 0 到 n-1 的范围内。
# 数组中某些数字是重复的，但不知道有几个数字是重复的。
# 也不知道每个数字重复几次。请找出数组中任意一个重复的数字。
# 例如，如果输入长度为 7 的数组 {2, 3, 1, 0, 2, 5, 3}，那么对应的输出是第一个重复的数字 2。

def timu1(a, n, b):
    if not isinstance(a, list):
        return
    print "ok"

    for i in a:
        if i not in b:
            b.append(i)
        else:
            print i
    print b


#
# 在一个二维数组中，每一行都按照从左到右递增的顺序排序，每一列都按照从上到下递增的顺序排序。请完成一个函数，输入这样的一个二维数组和一个整数，判断数组中是否含有该整数。
#
# Consider the following matrix:
# [
#   [1,   4,  7, 11, 15],
#   [2,   5,  8, 12, 19],
#   [3,   6,  9, 16, 22],
#   [10, 13, 14, 17, 24],
#   [18, 21, 23, 26, 30]
# ]
#
# Given target = 5, return true.
# Given target = 20, return false.

def timu2():
    a = [
        [1, 4, 7, 11, 15],
        [2, 5, 8, 12, 19],
        [3, 6, 9, 16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30]
    ]
    b = 6
    c = {'a', 'b', 'c', 'a', 'd'}
    print c
    for i in range(len(a)):
        if b in a[i]:
            print "true"
            break
    else:
        print "false"


def timu2G():
    a = [
        [1, 4, 7, 11, 15],
        [2, 5, 8, 12, 19],
        [3, 6, 9, 16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30]
    ]
    b = 6

    c, d = len(a), len(a[0])
    i = 0
    j = d - 1

    while i < c and j >= 0:
        print a[i][j]
        if a[i][j] == b:
            print "ok"
            break
        elif a[i][j] > b:
            j -= 1
        else:
            i += 1
    else:
        print "no"


# 请实现一个函数，将一个字符串中的空格替换成“%20”。例如，当字符串为 We Are Happy. 则经过替换之后的字符串为 We%20Are%20Happy。
def timu3():
    a = "We Are Happy"
    b = a.replace(" ", "%20")
    print b


def main():
    # timu1([2, 3, 1, 0, 2, 5, 3], 7, [])
    timu2()
    timu2G()
    timu3()
    # timu1()


if __name__ == '__main__':
    main()
