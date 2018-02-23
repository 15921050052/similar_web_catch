# -*- coding: utf-8 -*-
# similarWeb 详情解析


def detailBaseParse(spider, response):
    spider_name = spider.name
    spider.logInfo(spider_name)
    if False:
        spider.logWarn(u'访问过多被禁止')
        return None

    src_id = response.meta[u'src_id']
    search_word = response.meta[u'search_word']
    plat_name = response.meta[u'plat_name']
    hash_code = response.meta[u'hash_code']

    spider.saveFile(hash_code, response.body)

    source_url = response.url
    spider.logInfo(u'开始解析：%s' % plat_name + source_url)

    content = u''
    info = u''



    # content_item = {
    #     u'hash_code': hash_code,
    #     u'search_word': search_word,
    #     u'src_id': src_id,
    #     u'url': source_url,
    #     u'info': info,
    #     u'content': content
    # }
    #
    # return content_item


if __name__ == '__main__':
    pass