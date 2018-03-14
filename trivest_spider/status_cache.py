# -*- coding: utf-8 -*-
# 分为多个文件，防止出现同时操作文件的问题，以spiderName作为文件名
import json
import os
import shutil


def check(spider_name):
    # 判断当前文件是否存在，不存在，则新建
    file_name = spider_name + '.json'
    file_path = os.path.join(os.path.dirname(__file__) + '/status/')

    if not os.path.exists(file_path):
        os.mkdir(file_path)

    return file_path + file_name


# status状态有: '' 'stop' 'running'
def get_spider_status(spider_name):
    f = None
    file_detail_path = check(spider_name)
    try:
        if not os.path.exists(file_detail_path):
            # 不存在，则新建,并返回stop
            with open(file_detail_path, 'w') as f:
                json.dump({'status': 'stop'}, f)
            status = 'stop'
        else:
            with open(file_detail_path, 'r') as f:
                aa = json.load(f)
                status = aa.get('status', '')
    finally:
        if f:
            f.close()
    return status


def save_spider_status(spider_name, status):
    f = None
    file_detail_path = check(spider_name)
    try:
        with open(file_detail_path, 'w') as f:
            json.dump({'status': status}, f)
    finally:
        if f:
            f.close()


def clear_all_status():
    file_path = os.path.join(os.path.dirname(__file__) + '/status/')
    shutil.rmtree(file_path)
    os.mkdir(file_path)
