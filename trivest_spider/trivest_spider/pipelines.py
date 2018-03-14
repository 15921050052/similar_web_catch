# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import datetime

from trivest_data.dal import log_dao

from trivest_data.dal.trivest_spider import get_table_by_name


class BasePipeline(object):
    def __init__(self):
        self.belong_to = ''

    def log_info(self, msg, belong_to='', save_in_db=False):
        belong_to = belong_to or self.belong_to
        log_dao.info(msg, belong_to=belong_to, save_in_db=save_in_db)

    def log_warn(self, msg, belong_to='', save_in_db=True):
        belong_to = belong_to or self.belong_to
        log_dao.warn(msg, belong_to=belong_to, save_in_db=save_in_db)

    def process_item(self, item, spider):
        # 如果存储方式和process_item_default方法的相同，则直接调用父类的process_item_default
        item = self.process_item_default(item, self.Table, self.log_name)
        return item

    def close_spider(self, spider):
        pass

    def process_item_default(self, item, table, log_name):
        try:
            self.log_info(u'存%s详情：%s' % (log_name, item[u'search_word']), save_in_db=False)
            # 查重
            results = table.select().where(table.hash_code == item.get(u'hash_code')).count()
            if not results:
                item[u'update_time'] = datetime.datetime.now().strftime(u'%Y-%m-%d %H:%M:%S')
                table.create(**item)
                self.log_info(u'存%s详情：%s 成功' % (log_name, item[u'search_word'],))
            else:
                self.log_info(u'%s详情：%s 已经存在 ' % (log_name, item[u'search_word'],))
        except Exception as e:
            self.log_warn(str(e))
            self.log_warn(u'存%s详情：%s失败' % (log_name, item[u'search_word']))

        return item


class SimilarWebPipeline(BasePipeline):
    """
    similarWeb 详情
    """
    def __init__(self):
        self.belong_to = u'similar_detail'
        self.log_name = u'similarWeb'
        self.Table = get_table_by_name(u'similar_detail')