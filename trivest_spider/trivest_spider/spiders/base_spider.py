# -*- coding: utf-8 -*-
import time

import scrapy

from StatusCache import saveSpiderStatus
from trivest_data.dal import LogDao
from util import FileUtil
from util import NetworkUtil
from util import TimerUtil


# 封装基础方法
class BaseSpider(scrapy.Spider):
    def afterClose(self):
        # 如果正在爬，就不请求
        saveSpiderStatus(self.name, u'stop')
        self.logInfo(u'抓取结束-----------------' + self.name)

    def beforeRequest(self):
        # 如果正在爬，就不请求
        saveSpiderStatus(self.name, u'running')

    def logInfo(self, msg, belong_to='', saveInDB=False):
        belong_to = belong_to or self.name
        LogDao.info(msg, belong_to=belong_to, saveInDB=saveInDB)

    def logWarn(self, msg, belong_to='', saveInDB=False):
        belong_to = belong_to or self.name
        LogDao.warn(msg, belong_to=belong_to, saveInDB=saveInDB)

    def wait_utils_env_ok(self):
        # 检测网络
        while not NetworkUtil.checkNetWork():
            # 20s检测一次
            TimerUtil.sleep(20)
            self.logWarn(u'检测网络不可行')
            # continue

        # 检测服务器
        while not NetworkUtil.checkService():
            # 20s检测一次
            TimerUtil.sleep(20)
            self.logWarn(u'检测服务器不可行')
            # continue
        return True

    def dateFormat(self, dateStr='', targetFormat=''):
        if not dateStr:
            return ''
        dateStr = dateStr \
            .replace('\r\n', '') \
            .replace('\n', '') \
            .strip(' ') \
            .replace(u'年', '-') \
            .replace(u'月', '-') \
            .replace(u'日', ' ')
        needFormats = [
            u'%Y-%m-%d',
            u'%Y/%m/%d',
            u'%m/%d/%Y',
            u'%Y.%m.%d',
            u'%m/%d/%Y %H:%M:%S',
            u'%Y-%m-%d %H:%M',
            u'%Y-%m-%d %H:%M:%S',
            u'%Y/%m/%d %H:%M',
            u'%Y/%m/%d %H:%M:%S',
            u'%Y.%m.%d %H:%M:%S'
        ]
        targetFormat = targetFormat or u'%Y-%m-%d %H:%M:%S'
        for needFormat in needFormats:
            try:
                result = time.strftime(targetFormat, time.strptime(dateStr, needFormat))
                self.logInfo(u'匹配时间成功：' + result)
                return result
            except Exception as e:
                print str(e)
                continue
        return u''

    def saveFile(self, hash_code, content):
        if not FileUtil.dirIsExist(u'html'):
            FileUtil.createDir(u'html')
        filename = u'html/%s.html' % hash_code
        with open(filename, u'wb') as f:
            f.write(content.encode(u"utf8"))
        self.log(u'Saved file %s' % filename)
