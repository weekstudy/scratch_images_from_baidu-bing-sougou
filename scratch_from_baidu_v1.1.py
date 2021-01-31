#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@AUTHOR:
@FILE:scratch_from_baidu_v1.1.py
@NAME:
@TIME:2021/01/31
@IDE: PyCharm
@Ref:
"""


import re
import requests
import traceback
from multiprocessing import Pool
from scratch_images.utils import *


class ScratchImageFromBaidu(object):

    def __init__(self, ):
        self.urls_dir = './images_urls'
        self.images_dir = './images_baidu'
        self.headers = {'user-agent': 'Mozilla/5.0'}

    def get_image_urls(self, name, pages=2):
        page_id = 0
        urls = set()
        # 此处的参数为需爬取的页数
        for i in range(pages):
            # url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' \
            #       + self.name + "&pn=" + str(page_id) + "&gsm=?&ct=&ic=0&lm=-1&width=0&height=0"
            url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&' \
                  'logid=7115341739667250212&ipn=rj&ct=201326592&is=&fp=result&queryWord=' \
                  '{}&cl=&lm=&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&' \
                  'word={}&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&expermode=&' \
                  'force=&pn={}&rn=30&gsm=1e&1612100373755='.format(name, name, page_id)
            page_id += 30
            result = requests.get(url, headers=self.headers)
            urls_List = result.json()['data']
            i = 0
            for url_str in urls_List:
                i += 1
                try:
                    print(i, url_str['thumbURL'])
                    urls.add(url_str['thumbURL'])
                except Exception as e:
                    _ = e.__class__.__name__
                    # print(e.__class__.__name__)
                    traceback.print_exc()
                    continue

            # urls = result.content.decode(encoding='utf-8')
            # pic_url = re.findall('"objURL":"(.*?)",', urls, re.S, )
            # re = requests.post(urls)
            # todo 这里还要看看
            # pic_url = re.findall('"objURL":"(.*?)",', result.text, re.S, )
            # for url in pic_url:
            #     url2 = url.encode(encoding='unicode').decode(encoding='unicode')
            #     urls.add(url2)
            #     print(url2)
            # urls.add(pic_url)
        # urls =list(set(urls))
        print(len(urls))
        return list(urls)

    def get_images(self, pname, save_dir):

        pic_url = self.get_image_urls(pname,)
        i = 0
        print('找到关键词:' + pname + '的图片，现在开始下载图片...')

        for each in pic_url:
            i += 1
            print('正在下载第' + str(i) + '张图片，图片地址:' + str(each))
            image_name = save_dir + '/' + '%03d' % i + '.jpg'
            try:
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                pic = requests.get(each, headers=self.headers, timeout=10)
                with open(image_name, 'wb') as f:
                    f.write(pic.content)
                    f.close()
            except Exception as e:
                print(e.__class__.__name__)
                traceback.print_exc()
                print('【错误】当前图片无法下载')
                continue
        return i


if __name__ == '__main__':
    name_list = get_names()
    scratch_baidu = ScratchImageFromBaidu()
    # scratch_baidu.get_image_urls('美女',)
    for i in range(len(name_list)):
        images_urls = scratch_baidu.get_image_urls(name_list[i][5:],)
        write_urls2txt(name_list[i], images_urls, scratch_baidu.urls_dir, 'baidu')

        path = os.path.join(scratch_baidu.images_dir, name_list[i])
        scratch_baidu.get_images(name_list[i][5:], path)

