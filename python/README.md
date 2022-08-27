所有的语言都是帮助你去解决实际遇到的问题。

如果你只是简单的了解语言的特性 则很容易忘记。

想要学会怎么用这个语言，最好的方式是先找到需求，然后再找到解决方案。

比方说： 我要做一个一键替换整个文件夹下面的文件名称（当然是按照一定的规则去修改），这个时候的你才知道怎么去学去查，记住的东西则会更多，而不是为了学习而去学习

再比方说： 我想获取某个网站的图片的连接，该网站只有VIP才能下载，是否可以通过python去下载呢？

再比方说： 我想解决 12306 的图片验证码的相关问题

再比方说： 我想以图形化的方式呈现某种结果，可以是爬取出来的结果数据，可以是一段时间的折线图，可以是内存的增幅变化趋势等

再比方说： 我想获取网上的音乐资源连接，然后一段时间之后，需要判断连接是否有效。

这都是问题，而解决这些问题的方式，不应该仅仅局限于python语言。

语言知识一门工具，不同的语言对于相同的功能只有实现的难易方式的区别而已

总之： 需要有问题，再去解决问题，当然尽量往你需要学习的语言【取决于您的时间】身上去探索。
# server.py

文件 `server.py` 是在本地搭建一个本地服务器，供局域网的其他用户拉取或者上传文件的作用。

使用场景：

1. 有些设备只支持串口，设备只能使用U盘进行文件的拷贝，那么在这种场景就可以使用该脚本，车机需要上传日志给到电脑端进行查看，
2. 只有一台设备的情况下，可以进入设备进行拉取在局域网下的不同用户电脑里面的文件到车机设备上

可能需要安装 `tornado` 

可以单元测试

可以倒入库文件


# 基础类型
`[list]` 

| Method                                                       | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [append()](https://www.w3schools.com/python/ref_list_append.asp) | Adds an element at the end of the list                       |
| [clear()](https://www.w3schools.com/python/ref_list_clear.asp) | Removes all the elements from the list                       |
| [copy()](https://www.w3schools.com/python/ref_list_copy.asp) | Returns a copy of the list                                   |
| [count()](https://www.w3schools.com/python/ref_list_count.asp) | Returns the number of elements with the specified value      |
| [extend()](https://www.w3schools.com/python/ref_list_extend.asp) | Add the elements of a list (or any iterable), to the end of the current list |
| [index()](https://www.w3schools.com/python/ref_list_index.asp) | Returns the index of the first element with the specified value |
| [insert()](https://www.w3schools.com/python/ref_list_insert.asp) | Adds an element at the specified position                    |
| [pop()](https://www.w3schools.com/python/ref_list_pop.asp)   | Removes the element at the specified position                |
| [remove()](https://www.w3schools.com/python/ref_list_remove.asp) | Removes the item with the specified value                    |
| [reverse()](https://www.w3schools.com/python/ref_list_reverse.asp) | Reverses the order of the list                               |
| [sort()](https://www.w3schools.com/python/ref_list_sort.asp) | Sorts the list                                               |

### `(tuple)`

| Method                                                       | Description                                                  |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| [count()](https://www.w3schools.com/python/ref_tuple_count.asp) | Returns the number of times a specified value occurs in a tuple |
| [index()](https://www.w3schools.com/python/ref_tuple_index.asp) | Searches the tuple for a specified value and returns the position of where it was found |

`{set}`

| Method                                                       | Description                                                  |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| [add()](https://www.w3schools.com/python/ref_set_add.asp)    | Adds an element to the set                                   |
| [clear()](https://www.w3schools.com/python/ref_set_clear.asp) | Removes all the elements from the set                        |
| [copy()](https://www.w3schools.com/python/ref_set_copy.asp)  | Returns a copy of the set                                    |
| [difference()](https://www.w3schools.com/python/ref_set_difference.asp) | Returns a set containing the difference between two or more sets |
| [difference_update()](https://www.w3schools.com/python/ref_set_difference_update.asp) | Removes the items in this set that are also included in another, specified set |
| [discard()](https://www.w3schools.com/python/ref_set_discard.asp) | Remove the specified item                                    |
| [intersection()](https://www.w3schools.com/python/ref_set_intersection.asp) | Returns a set, that is the intersection of two other sets    |
| [intersection_update()](https://www.w3schools.com/python/ref_set_intersection_update.asp) | Removes the items in this set that are not present in other, specified set(s) |
| [isdisjoint()](https://www.w3schools.com/python/ref_set_isdisjoint.asp) | Returns whether two sets have a intersection or not          |
| [issubset()](https://www.w3schools.com/python/ref_set_issubset.asp) | Returns whether another set contains this set or not         |
| [issuperset()](https://www.w3schools.com/python/ref_set_issuperset.asp) | Returns whether this set contains another set or not         |
| [pop()](https://www.w3schools.com/python/ref_set_pop.asp)    | Removes an element from the set                              |
| [remove()](https://www.w3schools.com/python/ref_set_remove.asp) | Removes the specified element                                |
| [symmetric_difference()](https://www.w3schools.com/python/ref_set_symmetric_difference.asp) | Returns a set with the symmetric differences of two sets     |
| [symmetric_difference_update()](https://www.w3schools.com/python/ref_set_symmetric_difference_update.asp) | inserts the symmetric differences from this set and another  |
| [union()](https://www.w3schools.com/python/ref_set_union.asp) | Return a set containing the union of sets                    |
| [update()](https://www.w3schools.com/python/ref_set_update.asp) | Update the set with the union of this set and others         |

`{key:value}`

