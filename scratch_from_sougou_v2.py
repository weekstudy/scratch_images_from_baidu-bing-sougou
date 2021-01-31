#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@AUTHOR:
@FILE:scratch_from_search.py
@NAME:
@TIME:2021/01/31
@IDE: PyCharm

"""


import json

import requests
import socket
import ssl
import time
import traceback

from fake_useragent import UserAgent

from scratch_images.utils import *

# 设置请求超时时间，防止长时间停留在同一个请求
socket.setdefaulttimeout(10)
ssl._create_default_https_context = ssl._create_unverified_context


class ScratchImageFromSougou(object):

    def __init__(self):
        self.urls_dir = './images_urls'
        self.images_dir = './images_sougou'
        self.pages_num = 48
        self.headers = {'user-agent': UserAgent(verify_ssl=False).random}

    def get_image_urls(self, pname, total_img=144):
        imgs_urls = []
        mod = total_img % self.pages_num
        if mod == 0.0:
            pages_num = total_img // self.pages_num
        else:
            pages_num = total_img // self.pages_num + 1
        for i in range(pages_num):
            url = 'https://pic.sogou.com/pics?query={}' \
                  '&mode=1&start={}&reqType=ajax&reqFrom=result&tn=0' \
                .format(pname, i * self.pages_num)
            imgs = requests.get(url, headers=self.headers)
            jd = json.loads(imgs.text)
            jd = jd['items']
            for j in jd:
                imgs_urls.append(j['pic_url'])

        # print(len(imgs_urls))
        return list(set(imgs_urls))

    def get_images(self, pname, save_dir):

        images_urls = self.get_image_urls(pname,)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        for i, url in enumerate(images_urls):
            filename = os.path.join(save_dir, '%03d' % (i + 1) + '_sougou' + '.jpg')
            print(filename)
            with open(filename, 'wb+') as f:
                try:
                    f.write(requests.get(url, timeout=10).content)
                    time.sleep(0.5)
                except Exception as e:
                    print(e.__class__.__name__)
                    traceback.print_exc()
                    print('【图片无法下载】',url)
                    continue


if __name__ == '__main__':
    name_list = get_names()
    scratch_sougou = ScratchImageFromSougou()
    for i in range(len(name_list)):
        images_urls = scratch_sougou.get_image_urls(name_list[i][5:],)
        write_urls2txt(name_list[i], images_urls, scratch_sougou.urls_dir, 'sougou')

        path = os.path.join(scratch_sougou.images_dir, name_list[i])
        scratch_sougou.get_images(name_list[i][5:], path)

