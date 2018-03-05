# -*- coding: utf-8 -*-
import datetime
from scrapy import cmdline

# import logging
# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

spiderName = u'similar_web_loop'


cmdline.execute((u'scrapy crawl ' + spiderName + u' -s HTTPCACHE_ENABLED=0  ').split())

