# coding:utf-8


# 你好

def hello1():
    print "hello"


def hello2():
    from Test2 import world1
    print world1()


def compare(content, str):
    array = content.split("&*^*&&")
    array_combie = []
    for c in array:
        c = c.strip()
        if c == "":
            continue
        if "\t" in c:
            ca = c.split("\t")
            for cc in ca:
                if cc == "":
                    continue
                array_combie.append(cc)
        else:
            array_combie.append(c)

    for r in array_combie:
        print r
    return str.lower() in content.lower()


if __name__ == '__main__':
    # hello1()
    # hello2()
    print compare("TOTAL   123344    96692    21156\t\t\t0   139324    66317    30765", "total")
