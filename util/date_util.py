# -*- coding: utf-8 -*-
import time


def date_format(date_str='', target_format=''):
    """
    格式化时间
    :param date_str:
    :param target_format:
    :return: code, msg, data
    code: 200代表成功
    """
    msg = u'格式化失败'
    code = -100
    if not date_str:
        return -100, u'无时间字符串', None
    date_str = date_str \
        .replace('\r\n', '') \
        .replace('\n', '') \
        .strip(' ') \
        .replace(u'年', '-') \
        .replace(u'月', '-') \
        .replace(u'日', ' ')
    need_formats = [
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
    target_format = target_format or u'%Y-%m-%d %H:%M:%S'
    for needFormat in need_formats:
        try:
            result = time.strftime(target_format, time.strptime(date_str, needFormat))
            return 200, u'格式化时间成功', result
        except Exception as e:
            msg = str(e)
            continue
    return -100, msg, None


if __name__ == '__main__':
    pass
