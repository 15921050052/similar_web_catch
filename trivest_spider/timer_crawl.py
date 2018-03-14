# -*- coding: utf-8 -*-

import datetime
import subprocess

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from status_cache import clear_all_status, get_spider_status
from global_config import get_spider_detail, project_identify

import logging

# 为了处理：No handlers could be found for logger “apscheduler.scheduler”
# logging.basicConfig(level=logging.DEBUG)  # 不设置，就不打印


logging.basicConfig()


def start_spider(spider_name):
    print '执行', spider_name
    # return
    if get_spider_status(spider_name) != 'running':
        command = "scrapy crawl " + spider_name
        out_bytes = subprocess.check_output(command, shell=True)
        # print('end')
    else:
        print(spider_name + u' 还在抓取，跳过这轮start')


def similar_web():
    start_spider('similar_web_loop')


def start():
    # 当项目重新启动，清除所有状态
    clear_all_status()

    def add_job(func, timeSpace, delaySeconds=0):
        # 先马上开始执行
        # scheduler.add_job(func, 'date',misfire_grace_time=120) #misfire_grace_time=120,
        # 后再抓取之后的某个时间段开始间隔执行
        # next_run_time:设置下一轮开始时间
        # max_instances：如 1：表示当前方法正在执行还没有执行完，则不能再次启动这个方法，需等待完成，同理其他数
        # misfire_grace_time:120代表2分钟，当一个任务missing之后，在两分钟内会被重试
        scheduler.add_job(func, 'interval', seconds=timeSpace, misfire_grace_time=120,
                          next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=delaySeconds),
                          start_date=datetime.datetime.now() + datetime.timedelta(seconds=timeSpace), max_instances=1)

    timeSpace = 1 * 60
    # executors不设置，就会出现只能默认有5个线程
    executors = {
        'default': ThreadPoolExecutor(53+19),  # 根据任务数来定，每增加一个任务，就需要增加这个数量
        'processpool': ProcessPoolExecutor(53+19)
    }
    scheduler = BlockingScheduler(daemonic=False, executors=executors)
    add_job(similar_web, timeSpace)

    scheduler.start()


if __name__ == '__main__':
    start()
