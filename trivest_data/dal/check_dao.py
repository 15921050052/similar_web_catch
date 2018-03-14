# -*- coding: utf-8 -*-
from global_config import get_spider_detail

import log_dao
from trivest_data.dal.trivest_spider import get_table_by_name
from util import encrypt_util


class CheckDao(object):
    def __init__(self, spider_name):
        self.hash_list = []  # 代表此次已经存在的hash,防止同一时间得到相同文章进行抓取
        table_name = get_spider_detail(spider_name).get(u'table_name', '')
        self.Table = get_table_by_name(table_name)

    def reset_hash_list(self):
        # 每次重新抓取的时候清除
        self.hash_list = []

    def check_exist(self, source_url):
        """
        存在逻辑判断
        """
        hash_code = self.get_hash_code(source_url)
        try:
            results = self.Table.select().where(self.Table.hash_code == hash_code).count()
            if results or self.is_in_hash_list(hash_code):
                return True
            else:
                self.hash_list.append(hash_code)
                return False
        except Exception as e:
            log_dao.warn(str(e), belong_to='CheckDao')
            return False

    def is_in_hash_list(self, hash_code):
        return hash_code in self.hash_list

    def get_hash_code(self, source_url):
        # 具体逻辑
        return encrypt_util.md5(source_url)


if __name__ == '__main__':
    pass