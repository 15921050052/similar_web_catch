# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy.exceptions import CloseSpider

from base_spider import BaseSpider
from trivest_data.dal.CheckDao import CheckDao
from trivest_data.dal.trivest_spider import SimilarSrc
from util import NetworkUtil


class SimilarWebSpider(BaseSpider):
    """
    similarWeb抓取
    """
    name = u'similar_web'
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
        # while True:
        #     if self.is_running:
        #         continue
        #     self.is_running = True
        print u'第%s页面' % self.page
        src_list = SimilarSrc.select().paginate(self.page, 300)
        if not len(src_list):
            print u'第%s页面end' % self.page
        for src in src_list:
            plat_name = src.plat_name
            search_word = src.search_word
            src_id = src.id
            # new_url = 'http://blog.sina.com.cn/s/blog_166ae58120102xmxa.html'
            new_url = u'https://www.similarweb.com/website/%s' % search_word
            hash_code = self.checkDao.getHashCode(new_url)

            # if self.checkDao.checkExist(new_url):
            if self.checkFileExist(hash_code):
                self.logInfo(u'文章已经存在：' + new_url)
                continue

            self.logInfo(u"开始抓取详情：" + new_url)
            yield scrapy.Request(url=new_url,
                                 meta={
                                     u'request_type': self.name + u'_detail',
                                     u'plat_name': plat_name,
                                     u'search_word': search_word,
                                     u'src_id': src_id,
                                     u'hash_code': hash_code
                                 },
                                 callback=self.parseDetail, dont_filter=True)
        self.page += 1

    def parseDetail(self, response):
        self.logInfo(u'抓取返回')
        source_url = response.url
        if u'distil_r_captcha.html' in source_url:
            self.logWarn(u'被禁止了，重启路由，直接停止')
            NetworkUtil.getNewIp()
            raise CloseSpider(u'强制停止')
        hash_code = response.meta[u'hash_code']
        self.saveFile(hash_code, response.body)
        self.is_running = False
        time.sleep(10)
