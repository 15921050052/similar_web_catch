# -*- coding: utf-8 -*-
from pyexcel_xls import save_data


def save_xls_file(sheet_list, save_dir):
    from collections import OrderedDict
    data = OrderedDict()

    for sheet in sheet_list:
        sheet_name = sheet[u'sheet_name']
        rows = sheet[u'rows']
        # 添加sheet表
        data.update({sheet_name: rows})

    # 保存成xls文件
    save_data(save_dir, data)

if __name__ == '__main__':
    pass