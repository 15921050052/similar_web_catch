# -*- coding: utf-8 -*-
import datetime
from pyexcel_xls import get_data

from trivest_data.dal.trivest_spider import SimilarSrc


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
                # search_word = plat_url.rstrip(u'/#/') \
                #     .rstrip(u'/') \
                #     .lstrip(u'https://www.')\
                #     .lstrip(u'https://')\
                #     .lstrip(u'http://www.
                search_word = plat_url
                update_time = datetime.datetime.now().strftime(u'%Y-%m-%d %H:%M:%S')
                save(area, plat_name, plat_url, search_word, update_time, info)
        else:
            for page_data_item in page_data_list:
                plat_name = page_data_item[0]
                if u'平台名称' == plat_name:
                    continue
                plat_url = page_data_item[1]
                info = u''
                if len(page_data_item) >= 3:
                    info = page_data_item[2]
                # search_word = plat_url.rstrip(u'/')\
                #     .lstrip(u'https://www.')\
                #     .lstrip(u'https://')\
                #     .lstrip(u'http://www.')\
                #     .lstrip(u'http://')
                search_word = plat_url
                update_time = datetime.datetime.now().strftime(u'%Y-%m-%d %H:%M:%S')
                area = sheet_n
                save(area, plat_name, plat_url, search_word, update_time, info)


def save(area, plat_name, plat_url, search_word, update_time, info):
    print area, plat_name, plat_url, search_word
    SimilarSrc.create(**{
        u'area': area,
        u'plat_name': plat_name,
        u'plat_url': plat_url,
        u'search_word': search_word,
        u'update_time': update_time,
        u'info': info,
    })

if __name__ == '__main__':
    read_xls_file()
