# -*- coding: utf-8 -*-
from PIL import Image as image


def resize_img(**args):
    """
    等比例压缩图片
    使用案例：
    :param args:
    :return:
    """
    try:
        args_key = {'ori_img': '', 'dst_img': '', 'dst_w': '', 'dst_h': '', 'save_q': 100}
        arg = {}
        for key in args_key:
            if key in args:
                arg[key] = args[key]

        im = image.open(arg['ori_img'])
        if im.format in ['gif', 'GIF', 'Gif']:
            return
        ori_w, ori_h = im.size
        width_ratio = height_ratio = None
        ratio = 1
        if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):
            if arg['dst_w'] and ori_w > arg['dst_w']:
                width_ratio = float(arg['dst_w']) / ori_w  # 正确获取小数的方式
            if arg['dst_h'] and ori_h > arg['dst_h']:
                height_ratio = float(arg['dst_h']) / ori_h

            if width_ratio and height_ratio:
                if width_ratio < height_ratio:
                    ratio = width_ratio
                else:
                    ratio = height_ratio

            if width_ratio and not height_ratio:
                ratio = width_ratio
            if height_ratio and not width_ratio:
                ratio = height_ratio

            new_width = int(ori_w * ratio)
            new_height = int(ori_h * ratio)
        else:
            new_width = ori_w
            new_height = ori_h

        if len(im.split()) == 4:
            # prevent IOError: cannot write mode RGBA as BMP
            r, g, b, a = im.split()
            im = image.merge("RGB", (r, g, b))

        im.resize((new_width, new_height), image.ANTIALIAS).save(arg['dst_img'], quality=arg['save_q'])

    except Exception as e:
        raise ReSizeImgException(u'压缩失败:' + str(e))


class ReSizeImgException(Exception):
    """
    图片压缩异常
    """

    def __init__(self, msg):
        self.msg = msg


if __name__ == '__main__':
    pass
