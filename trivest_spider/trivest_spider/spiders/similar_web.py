# -*- coding: utf-8 -*-
import demjson
import scrapy

from base_spider import BaseSpider
from trivest_data.dal.CheckDao import CheckDao
from trivest_data.dal.trivest_spider import SimilarSrc
from trivest_spider.parse.SimilarWeb import detailBaseParse


class SimilarWebSpider(BaseSpider):
    """
    similarWeb抓取
    """
    name = u'similar_web'

    custom_settings = {
        u'download_delay': 2.5,
        u'ITEM_PIPELINES': {
            u'trivest_spider.pipelines.SimilarWebPipeline': 50,
        },
        u'handle_httpstatus_list': [204, 206, 301, 302, 400, 403, 404, 500]
    }

    def __init__(self, name=None, **kwargs):
        super(SimilarWebSpider, self).__init__(name=None, **kwargs)
        self.checkDao = CheckDao(self.name)
        self.css = {u'hash': u'style'}  # 用于缓存css

    def close(self, reason):
        # 做一些操作
        self.afterClose()

    def start_requests(self):
        # 做一些操作
        self.beforeRequest()

        if not self.wait_utils_env_ok():
            self.logWarn(u'环境不可行，退出当前抓取')
            return

        page = 1
        while True:
            print u'当前第%s页面' % page
            src_list = SimilarSrc.select().paginate(page, 1)
            if page == 2:
                break
            if not len(src_list):
                print u'第%s页面end' % page
                break
            for src in src_list:
                plat_name = src.plat_name
                search_word = src.search_word
                src_id = src.id
                new_url = u'https://www.similarweb.com/website/%s' % search_word
                hash_code = self.checkDao.getHashCode(new_url)

                if self.checkDao.checkExist(new_url):
                    self.logInfo(u'文章已经存在：' + new_url)
                    return

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
            page += 1

    def parseDetail(self, response):
        return detailBaseParse(self, response)
