# -*- coding: utf-8 -*-
from parse_html.parse import start
from util import file_util


def get_loop_cache():
    loop_cache = {
        u'last': {
            u'status': u'',
            u'dir': u'',
            u'time_start': u'',
            u'time_complete': u''
        },
        u'new': {
            u'status': u'',
            u'dir': u'',
            u'time_start': u'',
            u'time_complete': u''
        }
    }
    curr_path = file_util.get_curr_file_path(__file__)
    cache_path = file_util.join_path(file_util.get_father_path(curr_path), u'cache/loop_cache.json')
    code, msg, data = file_util.read_json_file(cache_path)
    if code == 200:
        return data
    else:
        return loop_cache


def start_parse_before():
    # 得到状态，存储地址
    loop_cache = get_loop_cache()

    last = loop_cache.get(u'last', {})
    new = loop_cache.get(u'new', {})
    status_last = last.get(u'status', u'')
    status_new = new.get(u'status', u'')

    if status_new == u'complete':
        # 说明需要解析
        dir = new.get(u'dir', u'')
    else:
        if status_last == u'complete':
            dir = last.get(u'dir', u'')
        else:
            return
    # 获取dir下面的所有html
    curr_path = file_util.get_curr_file_path(__file__)
    html_path = file_util.join_path(file_util.get_father_path(curr_path), 'html/' + dir)

    file_util.create_dir(u'result')
    start(html_path, u'result/%s.xls' % dir)


if __name__ == u'__main__':
    start_parse_before()