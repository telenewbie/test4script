# ecoding:utf-8
# 环境python 2.7
# 功能:对map进行排序
# http://mp.weixin.qq.com/s/fCPgV4fqxBVDia-sJZsmMQ

# 刷题
# 1)Project Euler
# 2)LeetCode

# 添加数据到Map中

# 无序字典
# ---------------------------------------
map = {'aa': 10, 'cc': 100, 'b': 200, 'bb': 2}

print(sorted(map.iteritems(), key=lambda x: x[0]))  # 表示按照key排序

print(sorted(map.iteritems(), key=lambda x: x[1]))  # 表示按照value排序

print(map)
# ---------------------------------------

# 有序字典
# ---------------------------------------
from collections import OrderedDict

orderDict = OrderedDict()
orderDict['a'] = 1
orderDict['b'] = 2
orderDict['c'] = 3
orderDict['d'] = 4
print(orderDict)
# ---------------------------------------

# 2.字典的取值 建议:尽量用dict.get()来代替dict[key]
# ---------------------------------------
# 因为dict['xx']如果xx不存在则会抛异常,而dict.get()则不会
print (map['aa'])
# print (map['c'])  # KeyError: 'c'
print (map.get('aa'))
print (map.get('c'))
# ---------------------------------------

# 3.字典中提取部分子集
# ---------------------------------------
students_score = {'jack': 80, 'james': 91, 'leo': 100, 'sam': 60}
# 提取分数超过90分的学生信息，并变成字典
# 我们可以用字典推导式，轻松搞定
good_score = {name: score for name, score in students_score.items() if score > 90}
print(good_score)
# ---------------------------------------


# 4.字典的计算
# ---------------------------------------
stocks = {'wanke': 25.6, 'wuliangye': 32.3, 'maotai': 299.5, 'huatai': 18.6}
print (min(stocks.values()))
print (max(stocks.values()))
new_stocks = zip(stocks.values(), stocks.keys())  # 进行翻转
print (new_stocks)
print (min(new_stocks))
print (max(new_stocks))
# ---------------------------------------

# 5.字典的翻转
# ---------------------------------------
from itertools import izip

invert_stocks2 = dict(izip(stocks.itervalues(), stocks.iterkeys()))
print(invert_stocks2)
# ---------------------------------------
# import itertools
#
#
# def predicate(x):
#     if (30 < x < 50):
#         return True
#     return False
#
#
# for x in itertools.takewhile(lambda x: 0 < x, stocks.values()):
#     print x
# # help(itertools.takewhile)

