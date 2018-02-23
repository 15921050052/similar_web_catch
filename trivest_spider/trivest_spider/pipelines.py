# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import datetime

from trivest_data.dal import LogDao

from trivest_data.dal.trivest_spider import getTableByName


class BasePipeline(object):
    def __init__(self):
        self.belong_to = ''

    def logInfo(self, msg, belong_to='', saveInDB=False):
        belong_to = belong_to or self.belong_to
        LogDao.info(msg, belong_to=belong_to, saveInDB=saveInDB)

    def logWarn(self, msg, belong_to='', saveInDB=True):
        belong_to = belong_to or self.belong_to
        LogDao.warn(msg, belong_to=belong_to, saveInDB=saveInDB)

    def process_item(self, item, spider):
        # 如果存储方式和process_item_default方法的相同，则直接调用父类的process_item_default
        item = self.process_item_default(item, self.Table, self.logName)
        return item

    def close_spider(self, spider):
        pass

    def process_item_default(self, item, table, logName):
        try:
            self.logInfo(u'存%s详情：%s' % (logName, item[u'search_word']), saveInDB=False)
            # 查重
            results = table.select().where(table.hash_code == item.get(u'hash_code')).count()
            if not results:
                item[u'update_time'] = datetime.datetime.now().strftime(u'%Y-%m-%d %H:%M:%S')
                table.create(**item)
                self.logInfo(u'存%s详情：%s 成功' % (logName, item[u'search_word'], ))
            else:
                self.logInfo(u'%s详情：%s 已经存在 ' % (logName, item[u'search_word'], ))
        except Exception as e:
            self.logWarn(str(e))
            self.logWarn(u'存%s详情：%s失败' % (logName, item[u'search_word']))

        return item


class SimilarWebPipeline(BasePipeline):
    """
    similarWeb 详情
    """
    def __init__(self):
        self.belong_to = u'similar_detail'
        self.logName = u'similarWeb'
        self.Table = getTableByName(u'similar_detail')