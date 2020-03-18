# coding:utf-8


# 你好

def hello1():
    print "hello"


def hello2():
    from Test2 import world1
    print world1()


if __name__ == '__main__':
    hello1()
    hello2()
