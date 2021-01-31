#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@AUTHOR:
@FILE:scratch_from_bing_v1.1.py
@NAME:
@TIME:2021/01/31
@IDE: PyCharm
@Ref:https://github.com/taojianglong/python-crawler
"""


import socket
import urllib
from bs4 import BeautifulSoup
import re
import time
import traceback
import ssl
from fake_useragent import UserAgent

from scratch_images.utils import *

# 设置请求超时时间，防止长时间停留在同一个请求
socket.setdefaulttimeout(10)
ssl._create_default_https_context = ssl._create_unverified_context


class ScratchImageFromBing(object):
    def __init__(self):
        self.urls_dir = './images_urls'
        self.images_dir = './images_bing'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
        self.re = re.compile(r"\"murl\"\:\"http\S[^\"]+")

    def get_img_urls(self, name, max_count=140, img_per_page=35):
        first = 1
        sfx = 1
        count = 0
        image_urls = []
        key = urllib.parse.quote(name)

        while count < max_count:

            url = "https://cn.bing.com/images/async?q={0}&first={1}&count={2}&scenario=ImageBasicHover&datsrc" \
                  "=N_I&layout=ColumnBased&mmasync=1&dgState=c*9_y*2226s2180s2072s2043s2292s2295s2079s2203s2094_i" \
                  "*71_w*198&IG=0D6AD6CBAF43430EA716510A4754C951&SFX={3}&iid=images.5599"\
                .format(key, first, img_per_page, sfx)

            # 正则表达式
            rule = re.compile(r"\"murl\"\:\"http\S[^\"]+")

            page = urllib.request.Request(url, headers=self.headers)
            # url = url.format(key, first, loadNum, sfx)
            html = urllib.request.urlopen(page)

            soup = BeautifulSoup(html, "lxml")
            link_list = soup.find_all("a", class_="iusc")
            urls = set()
            for link in link_list:
                result = re.search(rule, str(link))
                # 将字符串"amp;"删除
                img_url = result.group(0)
                # 组装完整url
                img_url = img_url[8:len(img_url)]
                urls.add(img_url)

            image_urls.extend(urls)
            count = len(image_urls)
            first = count + 1
            sfx += 1
        print(len(image_urls))
        for url in image_urls:
            print(url)

        return image_urls

    def get_images(self, pname, save_dir):

        """
         从原图url中将原图保存到本地
        """
        urls = self.get_img_urls(pname)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        for i, url in enumerate(urls):
            try:
                # 将网络对象复制到本地
                img_path = os.path.join(save_dir, '%03d' % (i + 1) + '_bing' + '.jpg')
                urllib.request.urlretrieve(url, img_path)
                time.sleep(0.5)
            except Exception as e:
                print(e.__class__.__name__)
                print(traceback.print_exc())

                time.sleep(0.5)
                print("产生了一点点错误，跳过...")
                continue
            else:
                print("图片+1,成功保存 " + str(i + 1) + " 张图")


if __name__ == '__main__':
    name_list = get_names()
    scratch_bing = ScratchImageFromBing()
    for i in range(len(name_list)):
        images_urls = scratch_bing.get_img_urls(name_list[i][5:], )
        write_urls2txt(name_list[i], images_urls, scratch_bing.urls_dir, 'bing')

        path = os.path.join(scratch_bing.images_dir, name_list[i])
        scratch_bing.get_images(name_list[i][5:], path)

