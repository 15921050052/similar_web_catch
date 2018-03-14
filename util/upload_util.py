# -*- coding: utf-8 -*-
from qcloud_cos import CosClient
from qcloud_cos import UploadFileRequest
from util import timer_util


class UploadUtil(object):
    def __init__(self, cos_path, local_path):
        appid = 1251316472  # 替换为用户的appid
        secret_id = u'AKID3atJdSnNR1Bwf1l4HnnYaSMzpBArC4A5'  # 替换为用户的secret_id
        secret_key = u'I2J7ho6wpQRRUpdX8K6KISBJCYSlm1hq'  # 替换为用户的secret_key
        region_info = "sh"  # 替换为用户的region，例如 sh 表示华东园区, gz 表示华南园区, tj 表示华北园区
        self.cos_client = CosClient(appid, secret_id, secret_key, region=region_info)
        self.cos_path = cos_path
        self.local_path = local_path

    def upload(self, path):
        """
        cos_path:/news/jiemian/image/
        :param path
        :return:
        """
        counter = 0
        url = ''
        while counter != 10:
            try:
                # 得到hash
                uploadName = path.replace('image\\', '')
                request = UploadFileRequest(u"crawler", self.cos_path + uploadName,
                                            self.local_path + path,
                                            insert_only=0)
                upload_file_ret = self.cos_client.upload_file(request)
                if upload_file_ret['code'] == 0:
                    data = upload_file_ret['data'] or {}
                    url = data['source_url']
                    print u'上传成功 ' + url
                else:
                    print u'上传图片失败', upload_file_ret
                break
            except Exception as e:
                counter += 1
                timer_util.sleep(10)
        return url


if __name__ == '__main__':
    pass