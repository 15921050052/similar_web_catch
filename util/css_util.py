# -*- coding: utf-8 -*-
import re
import requests
from csscompressor import compress
from util import encode_util


def download(url):
    try:
        result = requests.get(url, timeout=20)
        if result.status_code == 200:
            return encode_util.to_unicode(result.content)
        else:
            return ''
    except Exception, e:
        print e.message
        return ''


def compress_css(list_css):
    list_css = u''.join(list_css or [])
    return compress(list_css)


def clear_bg_color(value, color_list):
    for color in color_list:
        # background:#f3f3f3;
        p_all = re.compile('background\s*:\s*' + color + ';?')
        matches = p_all.findall(value)
        if len(matches):
            for match in matches:
                value = value.replace(match, '')
        # background-color:#f3f3f3;
        p_all = re.compile('background-color\s*:\s*' + color + ';?')
        matches = p_all.findall(value)
        if len(matches):
            for match in matches:
                value = value.replace(match, '')
    return value


def clear_url(value):
    # 替换样式里面的链接
    # url\(\s *\"?http.*?\"?\s*\)
    # url(http://storage.fedev.sina.com.cn/components/floatBarRight/40b6e9494c042dc1cb8682aac0e174d0.png)
    # url( "http://mat1.gtimg.com/www/images/channel_logo/tech_logo.png "  )
    # url(data:image/png;base64,iVBORw0KGgo)
    p_all = re.compile('url\(.*?\)')
    match_urls = p_all.findall(value)
    if len(match_urls):
        for matchUrl in match_urls:
            value = value.replace(matchUrl, u'url("")')

    # ngMethod=scale,src=http://www.sinaimg.cn/IT/deco/2014/0619/index/playIconH.png)}
    # # (src="https://mat1.gtimg.com/news/base2011/img/trs.png"
    p_all = re.compile('src=\".*\"|src=.*?\)')
    match_urls = p_all.findall(value)
    if len(match_urls):
        for matchUrl in match_urls:
            value = value.replace(matchUrl, u'src="")')
    return value
