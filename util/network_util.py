# -*- coding: utf-8 -*-
import urllib
import webbrowser


def open_web_browser(url):
    """
    打开浏览器
    :param url:
    :return:
    """
    webbrowser.open(url)


def check_net_work():
    """
        检测网络
    :return:boolean
    """
    try:
        response = urllib.urlopen('https://www.baidu.com')
        return response.code == 200
    except Exception:
        return False


def check_service():
    """
        检测服务器
    :return:boolean
    """
    return True


def get_new_ip():
    """
    重新获取IP
    :return:
    """
    try:
        response = urllib.urlopen(
            'http://localhost:9090/redial?token=qeelyn123!&from=localhost&app=TestRedialHttpServer&ver=1')
        return response.code == 200
    except Exception:
        return False
