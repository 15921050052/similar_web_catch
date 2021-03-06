# -*- coding: utf-8 -*-
# 项目唯一标识，分布式，不同的项目思考(规则：项目名称!@项目部署位置!@部署时间!@ 1000-9999的随机数）
project_identify = u'similarWeb!@xiamen!@2018-2-23 15:59!@7699'

# key为spider的名称 此配置和数据库：spider_monitor字段一致
spider_details = {
    u'similar_web_loop': {
        u'table_name': u'similar_detail',
        u'table_name_zh': u'SimilarWeb详情',
        u'spider_name': u'similar_web_loop',
        u'spider_name_zh': u'SimilarWeb 循环抓取'
    }
}


def get_spider_detail(spider_name):
    return spider_details.get(spider_name, {})