# encoding:utf-8
# 初次使用matplotlib
from matplotlib import pyplot as plt
import numpy as np
# 设置图像大小为8x6, 像素密度为80
plt.figure(figsize=(8, 6), dpi=80)
# 创建子图，1x1，在第一个位置，创建子图要在plot.plot()前面
plt.subplot(1, 1, 1)
X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
C, S = np.cos(X), np.sin(X)
#用蓝色的线，宽度为1.0来绘制cos函数
plt.plot(X, C, color="blue", linewidth=2.5, linestyle="-", label="test 1")
#用绿色的线，宽度为1.0来绘制sin函数
plt.plot(X, S, color="green", linewidth=2.5, linestyle="-", label="test 2")
#设置x轴的上下限
plt.xlim(-4.0, 4.0)
#设置x轴的坐标
plt.xticks(np.linspace(-4, 4, 9, endpoint=True))
# Set y limits
plt.ylim(-1.0, 1.0)
# Set y ticks
plt.yticks(np.linspace(-1, 1, 5, endpoint=True))
#保存图片，像素密度为72
# plt.savefig("exercice_2.png", dpi=72)
plt.legend(loc='upper left')

ax = plt.gca()  # 获取存在的轴心位置
#调整坐标轴的位置

ax.spines['right'].set_color('red')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data', 0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data', 0))

n = 1024
X = np.random.normal(0,1,n)
Y = np.random.normal(0,1,n)
plt.scatter(X,Y)

#在屏幕上显示出来
plt.show()

