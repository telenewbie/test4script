# coding:utf-8


def split(content, split1, split2):
    array = content.split(split1)
    array_combine = []
    for c in array:
        c = c.strip()
        if c == "":
            continue

        if split2 is not None and split2 in c:
            ca = c.split(split2)
            for cc in ca:
                if cc == "":
                    continue
                array_combine.append(cc)
        else:
            array_combine.append(c)

    return array_combine
