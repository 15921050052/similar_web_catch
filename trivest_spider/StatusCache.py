# -*- coding: utf-8 -*-
# 分为多个文件，防止出现同时操作文件的问题，以spiderName作为文件名
import json
import os
import shutil


def check(spiderName):
    # 判断当前文件是否存在，不存在，则新建
    fileName = spiderName + '.json'
    filePath = os.path.join(os.path.dirname(__file__) + '/status/')

    if not os.path.exists(filePath):
        os.mkdir(filePath)

    return filePath + fileName


# status状态有: '' 'stop' 'running'
def getSpiderStatus(spiderName):
    loadF = None
    fileDetailPath = check(spiderName)
    try:
        if not os.path.exists(fileDetailPath):
            # 不存在，则新建,并返回stop
            with open(fileDetailPath, 'w') as loadF:
                json.dump({'status': 'stop'}, loadF)
            status = 'stop'
        else:
            with open(fileDetailPath, 'r') as loadF:
                aa = json.load(loadF)
                status = aa.get('status', '')
    finally:
        if loadF:
            loadF.close()
    return status


def saveSpiderStatus(spiderName, status):
    loadF = None
    fileDetailPath = check(spiderName)
    try:
        with open(fileDetailPath, 'w') as loadF:
            json.dump({'status': status}, loadF)
    finally:
        if loadF:
            loadF.close()


def clearAllStatus():
    filePath = os.path.join(os.path.dirname(__file__) + '/status/')
    shutil.rmtree(filePath)
    os.mkdir(filePath)
