# encoding:utf-8
# http://blog.csdn.net/q583501947/article/details/76735870
from scipy import io as spio
from scipy import linalg
import numpy as np
# 这个模块可以加载和保存matlab文件：
filename = "file_scipy.mat"
a = np.ones((3, 3))
spio.savemat(filename, {'a': a})
data = spio.loadmat(filename)
print(data['a'])

arr = np.array([[3, 2], [3, 4]])
print(linalg.det(arr))
print(linalg.inv(arr))

# 快速傅里叶变换
time_np = 0.02
period = 5.
time_vec = np.arange(0, 20, time_np)
sig = np.sin(2*np.pi/period*time_vec)+0.5*np.random.randn(time_vec.size)
# print(sig)
from scipy import fftpack
sample_freq = fftpack.fftfreq(sig.size)
sig_fft = fftpack.fft(sig)
#print(sig_fft)

from matplotlib import pyplot as plt
def f(x):
    return x**2+10*np.sin(x)
x = np.arange(-10, 10, 0.1)
plt.plot(x, f(x))
# plt.show()

from scipy import optimize
optimize.fmin_bfgs(f, 0)
#用stats模块计算该分布的均值和标准差。
from scipy import stats
a = np.random.normal(size=1000)
loc, std = stats.norm.fit(a)
print(loc)
print(std)
print(np.median(a))


