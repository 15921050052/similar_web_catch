# -*- coding: utf-8 -*-


def get_coding(str_input):
    """
    获取编码格式
    """
    if isinstance(str_input, unicode):
        return "unicode"
    try:
        str_input.decode("utf8")
        return 'utf8'
    except:
        pass
    try:
        str_input.decode("gbk")
        return 'gbk'
    except:
        pass


def to_unicode(str_input):
    """
    得到unicode
    :return:
    """
    str_coding_fmt = get_coding(str_input)
    if str_coding_fmt == "utf8":
        return str_input.decode('utf8')
    elif str_coding_fmt == "unicode":
        return str_input
    elif str_coding_fmt == "gbk":
        return str_input.decode("gbk")


def tran2UTF8(str_input):
    """
    转化为utf8格式
    """
    str_coding_fmt = get_coding(str_input)
    if str_coding_fmt == "utf8":
        return str_input
    elif str_coding_fmt == "unicode":
        return str_input.encode("utf8")
    elif str_coding_fmt == "gbk":
        return str_input.decode("gbk").encode("utf8")


def tran2GBK(str_input):
    """
    转化为gbk格式
    """
    str_coding_fmt = get_coding(str_input)
    if str_coding_fmt == "gbk":
        return str_input
    elif str_coding_fmt == "unicode":
        return str_input.encode("gbk")
    elif str_coding_fmt == "utf8":
        return str_input.decode("utf8").encode("gbk")
