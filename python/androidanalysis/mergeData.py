# -*- coding:utf-8 -*-

def merge_x(iterables):
    # [[]]
    _set = set()
    for it in iterables:
        for x in it:
            _set.add(x)

    return sorted(_set)


def merge_y(x_list, x_name, y_name, iterables):
    # 依赖于 x 的个数
    # iterables 应该是个 字典[n:["x":[xxx]]["y":[xxx]]]

    # 取出 集合中是否存在 x_name 的项 ，如果存在则累加，如果不存在 不做处理

    _y = {}
    for i in x_list:
        _y[i] = 0
        pass
    # 进行合并
    for it in iterables:
        if iterables[it] is None:
            continue

        has_key_x = x_name in iterables[it]
        has_key_y = y_name in iterables[it]
        if has_key_x and has_key_y:
            same_key_len = len(iterables[it][x_name]) == len(iterables[it][y_name])
            if same_key_len:  # 长度相等才可以
                for x1 in iterables[it][x_name]:
                    if x1 in x_list:  # 存在在 集合中
                        # 计算在 原串 中的索引
                        # 判断 是否 存在 y坐标  ，并且是否越界
                        _y[x1] += iterables[it][y_name][iterables[it][x_name].index(x1)]
                        pass
                    pass
                pass

    _list = []
    for y in sorted(_y):
        _list.append(_y[y])
    return _list


def merge_y_1(x_list, x_name, y_name, iterables):
    '''
    如果不存在相应的 x坐标 则需要将 之前的值 进行累加

    :param x_list:
    :param x_name:
    :param y_name:
    :param iterables:
    :return:
    '''
    _y = {}
    for i in x_list:
        _y[i] = 0
        pass
    # 进行合并
    for it in iterables:
        if iterables[it] is None:
            continue
        has_key_x = x_name in iterables[it]
        has_key_y = y_name in iterables[it]
        if has_key_x and has_key_y:
            same_key_len = len(iterables[it][x_name]) == len(iterables[it][y_name])
            if same_key_len:  # 长度相等才可以
                success_find_index = 0
                for i in x_list:
                    if i in iterables[it][x_name]:
                        success_find_index = iterables[it][x_name].index(i)
                    # 取前一个值进行累加，如果没有前一个值则默认为0
                    _y[i] += iterables[it][y_name][success_find_index]
                    # print "第 %s 个值:%s,加入进来的值：%s" % (i, _y[i], iterables[it][y_name][success_find_index])
                    pass

    _list = []
    for y in sorted(_y):
        _list.append(_y[y])
    return _list
