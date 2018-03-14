# -*- coding: utf-8 -*-
import json
import os
import time

import scrapy

from status_cache import save_spider_status
from trivest_data.dal import log_dao
from util import file_util
from util import network_util
from util import timer_util


# 封装基础方法
class BaseSpider(scrapy.Spider):
    def after_close(self):
        # 如果正在爬，就不请求
        save_spider_status(self.name, u'stop')
        self.log_info(u'抓取结束-----------------' + self.name)

    def before_request(self):
        # 如果正在爬，就不请求
        save_spider_status(self.name, u'running')

    def log_info(self, msg, belong_to='', save_in_db=False):
        belong_to = belong_to or self.name
        log_dao.info(msg, belong_to=belong_to, save_in_db=save_in_db)

    def log_warn(self, msg, belong_to='', save_in_db=False):
        belong_to = belong_to or self.name
        log_dao.warn(msg, belong_to=belong_to, save_in_db=save_in_db)

    def wait_utils_env_ok(self):
        # 检测网络
        while not network_util.check_net_work():
            # 20s检测一次
            timer_util.sleep(20)
            self.log_warn(u'检测网络不可行')
            # continue

        # 检测服务器
        while not network_util.check_service():
            # 20s检测一次
            timer_util.sleep(20)
            self.log_warn(u'检测服务器不可行')
            # continue
        return True

    def save_html_file(self, dir, hash_code, content):
        file_util.create_dir('html')
        code, msg, data = file_util.save_txt_file('html/'+dir, hash_code+'.html', content)
        if code == 200:
            self.log_info(u'Saved file %s' % data)
        else:
            self.log_warn(u'Saved file %s fail' % data)

    def save_loop_cache_file(self, loop_cache):
        code, msg, data = file_util.save_json_file('cache', 'loop_cache.json', loop_cache)
        if code == 200:
            self.log_info(u'Saved file %s' % data)
        else:
            self.log_warn(u'Saved file %s fail' % data)

    def get_loop_cache(self):
        f = None
        loop_cache = {
            u'last': {
                u'status': u'',
                u'dir': u'',
                u'time_start': u'',
                u'time_complete': u''
            },
            u'new': {
                u'status': u'',
                u'dir': u'',
                u'time_start': u'',
                u'time_complete': u''
            }
        }
        code, msg, data = file_util.read_json_file(u'cache/loop_cache.json')
        if code == 200:
            return data
        else:
            self.log_info(msg)
            return loop_cache

