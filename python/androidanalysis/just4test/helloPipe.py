# coding:utf-8

from multiprocessing import Process, Pipe, Value
import thread
import time


def childprocess(conn):
    # 开个线程 每隔1s写1次
    thread.start_new_thread(child_do, (conn,))
    while (True):
        time.sleep(1)


def child_do(conn):
    while (True):
        info = conn.recv()
        print info.toString()


class Info():
    """
    携带的数据，给到另外一个进程
    需要跨进程，进行交互，
    """
    isStop = Value("b", False)
    mode = 1  # 老化模式
    wifi_change_interval = 0  # wifi定时改变的间隔，0为不启用
    process_names = []  # 进程名称
    change_pcm_interval = 5 * 60  # 切换音频集之间是否间隔  默认5分钟
    change_pcm_list_interval = 2 * 60 * 60  # 是否切换音频集 默认2 小时
    interval_pcm = 1  # 采集 pcm 的间隔
    interval_mem = 1  # 采集 内存的间隔
    keep_save_data_timeout = 10 * 60  # 是否指定 静态数据的抓取 的耗时时间

    def toString(self):
        return "isStop = " + str(self.isStop.value) + ", mode = " + str(self.mode)

    pass


info = Info()


def other_child(conn):
    while (True):
        info = conn.recv()
        print "other:" + info.toString()


if __name__ == '__main__':
    recv_conn, write_conn = Pipe()
    p = Process(target=childprocess, args=(recv_conn,))
    p.start()
    p1 = Process(target=other_child, args=(recv_conn,))
    p1.start()
    # 一直读，每隔 0.4s读一次
    while (True):
        write_conn.send(info)
        info.isStop.value = not info.isStop.value
        print ("parent :" + str(info.isStop.value))
        time.sleep(1)

    p.join()
