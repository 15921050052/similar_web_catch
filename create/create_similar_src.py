# -*- coding: utf-8 -*-
import datetime
import urlparse

from pyexcel_xls import get_data, save_data

from trivest_data.dal.trivest_spider import SimilarSrc
from util import EncryptUtil


def read_xls_file():
    xls_data = get_data(r"src.xlsx")
    for sheet_n in xls_data.keys():
        page_data_list = xls_data[sheet_n]
        if u'其他地区' == sheet_n:
            for page_data_item in page_data_list:
                area = page_data_item[0]
                plat_name = page_data_item[1]
                if u'平台名称' == plat_name:
                    continue
                plat_url = page_data_item[2]
                info = u''
                if len(page_data_item) >= 4:
                    info = page_data_item[3]
                search_word = urlparse.urlsplit(plat_url).netloc.replace(u'www.', u'')
                hash_code = EncryptUtil.md5(u'https://www.similarweb.com/website/%s' % search_word)
                update_time = datetime.datetime.now().strftime(u'%Y-%m-%d %H:%M:%S')
                save(hash_code, area, plat_name, plat_url, search_word, update_time, info)
        else:
            for page_data_item in page_data_list:
                plat_name = page_data_item[0]
                if u'平台名称' == plat_name:
                    continue
                plat_url = page_data_item[1]
                info = u''
                if len(page_data_item) >= 3:
                    info = page_data_item[2]
                search_word = urlparse.urlsplit(plat_url).netloc.replace(u'www.', u'')
                # search_word = plat_url
                hash_code = EncryptUtil.md5(u'https://www.similarweb.com/website/%s' % search_word)

                update_time = datetime.datetime.now().strftime(u'%Y-%m-%d %H:%M:%S')
                area = sheet_n
                save(hash_code, area, plat_name, plat_url, search_word, update_time, info)


def save(hash_code, area, plat_name, plat_url, search_word, update_time, info):
    print hash_code, area, plat_name, plat_url, search_word
    SimilarSrc.create(**{
        u'hash_code': hash_code,
        u'area': area,
        u'plat_name': plat_name,
        u'plat_url': plat_url,
        u'search_word': search_word,
        u'update_time': update_time,
        u'info': info,
    })

if __name__ == '__main__':
    read_xls_file()