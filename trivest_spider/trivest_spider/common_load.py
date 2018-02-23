# -*- coding: utf-8 -*-
import time

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException

from trivest_data.dal.trivest_spider import SimilarSrc
from util import EncryptUtil
from util import FileUtil


def getPhantomJs():
    service_args = [u'--load-images=no', u'--disk-cache=yes', u'--ignore-ssl-errors=true']
    driver = webdriver.PhantomJS(service_args=service_args)
    return driver


def load(url):
    print u'开始加载'

    def wait_for_load(a_driver):
        element = a_driver.find_element_by_tag_name(u'html')
        count = 0
        while True:
            count += 1
            # 超过5s，直接返回,看情况设置
            if count > 5:
                print(u'Timing out after 5s and returning')
                return
            print u'睡眠1s'
            time.sleep(0.5)  # 检查还是不是同一个element，如果不是，说明这个html标签已经不再DOM中了。如果不是抛出异常
            new = a_driver.find_element_by_tag_name(u'html')
            if element != new:
                raise StaleElementReferenceException(u'刚才重定向了！')

    driver = getPhantomJs()
    driver.get(url)
    try:
        wait_for_load(driver)
    except StaleElementReferenceException as e:
        print e.msg
    finally:
        return 200, u'成功', {
            u'source_url': driver.current_url,
            u'html': driver.page_source,
        }


def saveFile(hash_code, content):
    if not FileUtil.dirIsExist(u'html'):
        FileUtil.createDir(u'html')
    filename = u'html/%s.html' % hash_code
    with open(filename, u'wb') as f:
        f.write(content.encode(u"utf8"))


if __name__ == '__main__':
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
            hash_code = EncryptUtil.md5(new_url)
            print new_url
            code, msg, data = load(new_url)
            html = data.get(u'html', u'')
            saveFile(hash_code, html)
        page += 1
