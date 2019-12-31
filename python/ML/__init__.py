# encoding:utf-8
# 使用numpy ,numpy提供了一套的数学函数
# http://blog.csdn.net/q583501947/article/details/76637765
import numpy as np

a = np.array([1, 2, 3])
print(type(a))
# 数组的纬度
print(a.shape)
# 数组轴的个数
print(a.ndim)
# 元素类型
print(a.dtype)
# 元素的字节大小
print(a.itemsize)
print(a.real)
print(a[0], a[1])
a[0] = 6
print(a)

b = np.array([[1, 2, 3], [4, 5, 6]])
print(b)
print(b.shape)
print(b[0][0])

e = np.random.random_integers(1, 10, (2, 2))
print(e)
