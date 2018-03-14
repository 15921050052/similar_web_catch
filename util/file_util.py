# -*- coding: utf-8 -*-
import json
import os


def get_curr_path():
    """
    获取当前工作目录
    :return:
    """
    return os.getcwd()


def get_curr_file_path(__file__):
    """
    获取当前文件所在目录
    :param __file__: 对应文件的file变量
    :return:
    """
    return os.path.dirname(__file__)


def get_father_path(sub_path):
    """
    获取父目录
    :param sub_path: 子路径
    :return:
    """
    return os.path.dirname(sub_path)


def join_path(dir, file_name):
    return os.path.join(dir, file_name)


def file_is_exist(path_and_name):
    return os.path.exists(path_and_name)


def dir_is_exist(path):
    return os.path.isdir(path)


def create_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def del_file(path):
    if file_is_exist(path):
        os.remove(path)


def get_all_file_path(path):
    path_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        # print ''.join(os.path.splitext(file))
        file_name = os.path.splitext(file)[0]
        file_name_all = ''.join(os.path.splitext(file))
        if os.path.isdir(file_path):
            get_all_file_path(file_path)
        else:
            path_list.append([file_path, file_name, file_name_all])
    return path_list


def get_all_file_name(path):
    name_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        file_name = os.path.splitext(file)[0]
        if os.path.isdir(file_path):
            get_all_file_path(file_path)
        else:
            name_list.append(file_name)
    return name_list


def read_file(file_path):
    f = None
    msg = u'没有读取到文件内容'
    try:
        with open(file_path, u'r') as f:
            return -200, u'成功读取', f.read()
    except Exception, e:
        msg = str(e)
    finally:
        f and f.close()
    return -100, msg, None


def read_json_file(file_path):
    f = None
    msg = u'没有读取到文件内容'
    try:
        with open(file_path, u'r') as f:
            return -200, u'成功读取', json.load(f)
    except Exception, e:
        msg = str(e)
    finally:
        f and f.close()
    return -100, msg, None


def save_txt_file(dir, file_name, txt):
    f = None
    msg = u'没能成功存储'
    data = None
    try:
        if not dir_is_exist(dir):
            create_dir(dir)
        data = path = join_path(dir, file_name)
        with open(path, u'w') as f:
            f.write(txt.encode(u"utf8"))
            return 200, u'成功存入', path
    except Exception, e:
        msg = str(e)
    finally:
        f and f.close()
    return -100, msg, data


def save_json_file(dir, file_name, json_obj):
    f = None
    msg = u'没能成功存储'
    data = None
    try:
        if not dir_is_exist(dir):
            create_dir(dir)
        data = path = join_path(dir, file_name)
        with open(path, u'w') as f:
            json.dump(json_obj, f)
            return 200, u'成功存入', path
    except Exception, e:
        msg = str(e)
    finally:
        f and f.close()
    return -100, msg, data
