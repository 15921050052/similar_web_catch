# -*- coding: utf-8 -*-
import datetime
import os
import time

import scrapy
from scrapy.exceptions import CloseSpider

from base_spider import BaseSpider
from trivest_data.dal.CheckDao import CheckDao
from trivest_data.dal.trivest_spider import SimilarSrc
from util import NetworkUtil


class SimilarWebSpider(BaseSpider):
    """
    similarWeb 循环抓取
    """
    name = u'similar_web_loop'
    handle_httpstatus_list = [204, 206, 301, 400, 403, 404, 405, 500]
    custom_settings = {
        u'ITEM_PIPELINES': {
            u'trivest_spider.pipelines.SimilarWebPipeline': 50,
        }
    }

    def __init__(self, name=None, **kwargs):
        super(SimilarWebSpider, self).__init__(name=None, **kwargs)
        self.checkDao = CheckDao(self.name)
        self.css = {u'hash': u'style'}  # 用于缓存css
        self.page = 1
        self.is_running = False

    def close(self, reason):
        # 做一些操作
        self.afterClose()

    def start_requests(self):
        # 做一些操作
        self.beforeRequest()

        if not self.wait_utils_env_ok():
            self.logWarn(u'环境不可行，退出当前抓取')
            return
        print u'开始执行'

        loop_cache = self.getLoopCache()
        dir_str = datetime.datetime.now().strftime(u'%Y_%m_%d_%H_%M_%S')
        curr_time_str = datetime.datetime.now().strftime(u'%Y-%m-%d %H:%M:%S')
        is_monday = datetime.datetime.now().weekday() == 0
        is_tuesday = datetime.datetime.now().weekday() == 1

        last = loop_cache.get(u'last', {})
        new = loop_cache.get(u'new', {})
        status = new.get(u'status', u'')
        time_start = new.get(u'time_start', u'')
        time_complete = new.get(u'time_complete', u'')
        self.logInfo(u'status：%s' % (status, ))
        if not status:
            # 说明需要重新抓取，存取的路径为dir_str
            new = {
                u'status': u'loading',
                u'dir': dir_str,
                u'time_start': curr_time_str,
                u'time_complete': u''
            }
            self.logInfo(u'不存在状态，新建')
        else:
            if status == u'complete':
                self.logInfo(u'is_monday：%s，is_tuesday：%s' % (is_monday, is_tuesday))
                if not is_monday and not is_tuesday:
                    # 完成状态下，不是周一，周二，就直接退出不抓
                    self.logInfo(u'不是周一周二，不抓取')
                    return
                # 完成抓取的时间
                curr_time = datetime.datetime.now()
                time_complete = datetime.datetime.strptime(time_complete, u'%Y-%m-%d %H:%M:%S')
                space_day = (curr_time - time_complete).days
                if space_day <= 1:
                    # 小于等于1天，说明周一刚抓完
                    self.logInfo(u'小于等于1天，说明周一刚抓完')
                    return
                # 如果是完成状态，且是周一 周二 说明需要重新抓取
                last = new
                new = {
                    u'status': u'loading',
                    u'dir': dir_str,
                    u'time_start': curr_time_str,
                    u'time_complete': u''
                }
        # 存入状态数据
        loop_cache = {
            u'last': last,
            u'new': new
        }
        self.saveLoopCacheFile(loop_cache)
        src_list = SimilarSrc.select().paginate(self.page, 300)
        has_req = False
        for src in src_list:
            plat_name = src.plat_name
            search_word = src.search_word
            src_id = src.id
            new_url = u'https://www.similarweb.com/website/%s' % search_word
            hash_code = self.checkDao.getHashCode(new_url)

            if os.path.exists(u'html/%s/%s.html' % (new.get(u'dir', ''), hash_code)):
                self.logInfo(u'文章已经存在：' + new_url)
                continue
            has_req = True
            self.logInfo(u"开始抓取详情：" + new_url)
            yield scrapy.Request(url=new_url,
                                 meta={
                                     u'request_type': self.name + u'_detail',
                                     u'plat_name': plat_name,
                                     u'search_word': search_word,
                                     u'src_id': src_id,
                                     u'hash_code': hash_code,
                                     u'src_list': src_list,
                                     u'new': new,
                                     u'loop_cache': loop_cache
                                 },
                                 callback=self.parseDetail, dont_filter=True)

        # 全部走完之后, 没有进行请求的，都要判断一下文件
        not has_req and self.checkAllSave(new, src_list, loop_cache)

    def checkAllSave(self, new, src_list, loop_cache):
        # 存储成功之后，判断所有文件是否下载全
        file_name_list = self.get_all_file_name(u'html/%s/' % (new.get(u'dir', u''),))

        all_save = True
        for src in src_list:
            hash_code = src.hash_code
            if hash_code not in file_name_list:
                all_save = False
                break
        if all_save:
            # 如果全部下载完成了，更新new为complete
            new[u'status'] = u'complete'
            new[u'time_complete'] = datetime.datetime.now().strftime(u'%Y-%m-%d %H:%M:%S')
            loop_cache[u'new'] = new
            self.saveLoopCacheFile(loop_cache)
            self.logInfo(u'一轮全部完成抓取')

    def parseDetail(self, response):
        self.logInfo(u'抓取返回')
        src_list = response.meta[u'src_list']
        new = response.meta[u'new']
        loop_cache = response.meta[u'loop_cache']
        source_url = response.url
        if u'distil_r_captcha.html' in source_url:
            self.logWarn(u'被禁止了，重启路由，直接停止')
            NetworkUtil.getNewIp()
            raise CloseSpider(u'强制停止')
        hash_code = response.meta[u'hash_code']
        self.saveHtmlFile(new.get(u'dir', u''), hash_code, response.body)

        self.checkAllSave(new, src_list, loop_cache)
        self.is_running = False
        time.sleep(10)
