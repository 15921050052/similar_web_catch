# -*- coding: utf-8 -*-


def i_e(condition, yes, no):
    """
    仿照三元操作符
    :param condition:
    :param yes:
    :param no:
    :return:
    """
    return yes if condition else no


def l_i(condition, list, yes_index, no):
    """
    根据条件，获取数组的第几个
    :param condition:
    :param list:
    :param yes_index:
    :param no:
    :return:
    """
    return list[yes_index] if condition else no


if __name__ == '__main__':
    pass
