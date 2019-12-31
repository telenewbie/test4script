#ecoding:utf-8
# 这个是http://www.runoob.com/python/python-exercise-example1.html的例子
def demo1():
    for i in range(1,5):
        for j in range(1,5):
            for k in range(1,5):
                if(i!=j and j!=k and i!=k):
                    print i,j,k
#demo2比demo2xxx的效率要慢！！！
def demo2(i):
    while(i):
        if(i<=10):
            return i*0.1
        elif(i>10 and i<=20):
            return (i-10)*0.075+demo2(10)
        elif(i>20 and i<=40):
            return (i-20)*0.05+demo2(20)
        elif (i > 40 and i <= 60):
            return (i - 40) * 0.03 + demo2(40)
        elif (i > 60 and i <= 100):
            return (i - 60) * 0.015 + demo2(60)
        elif (i >100):
            return (i - 100) * 0.01 + demo2(100)
def demo2xxx(i):
    arr = [1000000, 600000, 400000, 200000, 100000, 0]
    rat = [0.01, 0.015, 0.03, 0.05, 0.075, 0.1]
    r = 0
    print demo2(i)
    i = i * 10000
    for idx in range(0, 6):
        if i > arr[idx]:
            r += (i - arr[idx]) * rat[idx]
            # print (i - arr[idx]) * rat[idx]
            i = arr[idx]
    print r


# print demo2xxx(12)

def demo3():#有没有更加方便的方式
    import  math
    for i in range(10000):
        x=int(math.sqrt(i+100))
        y=int(math.sqrt(i+268))
        if(x*x==i+100 and y*y ==i+268):
            print i
demo3()