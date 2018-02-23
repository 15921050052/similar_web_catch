# -*- coding: utf-8 -*-
import random
import time

import requests

from trivest_data.dal.trivest_spider import SimilarSrc
from util import EncryptUtil
from util import FileUtil

USER_AGENTS = [
    u'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
]


def saveFile(hash_code, content):
    if not FileUtil.dirIsExist(u'html'):
        FileUtil.createDir(u'html')
    filename = u'html/%s.html' % hash_code
    with open(filename, u'wb') as f:
        f.write(content)
        f.close()
    print u'存储完成'


def load(url):
    headers = {
        u'User-Agent': random.choice(USER_AGENTS)
    }
    result = requests.get(url, timeout=20, headers=headers)
    result.encoding = u'utf-8'
    # print result.content
    return result.content


if __name__ == '__main__':
    page = 4
    is_running = False
    while True:
        if is_running:
            continue
        is_running = True

        print u'当前第%s页面' % page
        src_list = SimilarSrc.select().paginate(page, 1)
        # if page == 3:
        #     break
        if not len(src_list):
            print u'第%s页面end' % page
            break
        for src in src_list:
            plat_name = src.plat_name
            search_word = src.search_word
            src_id = src.id
            new_url = u'https://www.similarweb.com/website/%s' % search_word
            hash_code = EncryptUtil.md5(new_url)
            print new_url
            html = load(new_url)
            saveFile(hash_code, html)
        page += 1
        is_running = False
        print u'睡一下'
        time.sleep(20)
