# coding=utf-8

from androidanalysis.config.Constant import *

class Info:
    """
    携带的数据，给到另外一个进程
    需要跨进程，进行交互，
    """

    def __init__(self):
        pass

    mode = 1  # 老化模式
    wifi_change_interval = DEFAULT_INTERVAL_CHANGE_WIFI  # wifi定时改变的间隔，0为不启用
    process_names = ""  # 进程名称
    change_pcm_interval_continue = DEFAULT_INTERVAL_CHANGE_PCM_CONTINUE  # 切换音频集 持续多久时间  默认5分钟
    change_pcm_list_interval = DEFAULT_INTERVAL_CHANGE_PCM  # 是否切换音频集 默认2 小时
    interval_cpu = DEFAULT_INTERVAL_CPU  # 采集 cpu 的间隔
    interval_pid_fd_task = DEFAULT_INTERVAL_PID  # 采集 cpu 的间隔
    interval_mem = DEFAULT_INTERVAL_MEM  # 采集 内存的间隔
    interval_pull_log = DEFAULT_INTERVAL_PULL_LOG  # 采集 log的间隔
    keep_save_data_timeout = DEFAULT_INTERVAL_SAVE_DATA  # 是否指定 静态数据的抓取 的耗时时间
    dev = ""  # 设备名称

    def is_open_change_pcm_list(self):
        """
        是否打开 切换音频集合
        :return: 是否
        """
        return self.change_pcm_list_interval > 0

    def is_open_change_pcm_list_interval(self):
        """
        是否打开 音频集合切换的间隔
        :return:
        """
        return self.change_pcm_interval > 0

    pass
