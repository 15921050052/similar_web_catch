# -*- coding: utf-8 -*-
from GlobleConfig import getSpiderDetail

import LogDao
from trivest_data.dal.trivest_spider import getTableByName
from util import EncryptUtil


class CheckDao(object):
    def __init__(self, spiderName):
        self.hashList = []  # 代表此次已经存在的hash,防止同一时间得到相同文章进行抓取
        tableName = getSpiderDetail(spiderName).get(u'table_name', '')
        self.Table = getTableByName(tableName)

    def resetHashList(self):
        # 每次重新抓取的时候清除
        self.hashList = []

    def checkExist(self, source_url):
        """
        存在逻辑判断
        """
        hash_code = self.getHashCode(source_url)
        try:
            results = self.Table.select().where(self.Table.hash_code == hash_code).count()
            if results or self.isInHashList(hash_code):
                return True
            else:
                self.hashList.append(hash_code)
                return False
        except Exception as e:
            LogDao.warn(str(e), belong_to='CheckDao')
            return False

    def isInHashList(self, hash_code):
        return hash_code in self.hashList

    def getHashCode(self, source_url):
        # 具体逻辑
        return EncryptUtil.md5(source_url)


if __name__ == '__main__':
    pass