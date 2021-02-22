#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
"""
@AUTHOR:
@FILE:main.py
@NAME:my_insightface
@TIME:2021/02/01
@IDE: PyCharm
@Ref:
"""

from concurrent.futures import ThreadPoolExecutor
import json
from lxml import etree
import os
import requests
import sys
import time
import traceback
from multiprocessing import Pool


sys.path.append('..')
from scratch_images.utils import *


requests.DEFAULT_RETRIES = 15
requests.DEFAULT_POOLSIZE = 100
SAVE_IMAGES_DIR = './images3'


def get_image(image_url_name):
    """
    获取网页图片
    :param image_url_name:
    :return:
    """
    url = image_url_name[0]
    image_name = image_url_name[1]
    # pname = os.path.split(image_name)[1]
    pname = os.path.dirname(image_name)
    # sess = requests.session()
    # sess.keep_alive = False
    # print(url)
    try:
        image_bytes = requests.get(url, timeout=10, allow_redirects=False).content
        # sess.close()
    except Exception as e:
        print(e.__class__.__name__)
        traceback.print_exc()
        print(pname, url, '网页无法访问……')
        return None

    with open(image_name, 'wb+') as fw:
        print('正在下载', pname, url)
        fw.write(image_bytes)
    # time.sleep(0.01)
    return None


def get_images_ulrs_from_baidu(name0, pages=1, save_dir=SAVE_IMAGES_DIR, thread_workers=3):
    """
    获取百度图片每页的url
    :param thread_workers:
    :param save_dir:
    :param name0:
    :param pages:
    :return:
    """

    enginee = 'baidu'
    save_dir = os.path.join(save_dir, enginee)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 用来判断哪些人已经爬取过了
    names = sorted(os.listdir(save_dir))
    if name0 in names:
        print(enginee + '_' + name0 + '_scratched')
        return None

    # 人物图片存放的路劲
    save_dir = os.path.join(save_dir, name0)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    pname = name0.split('_')[1]
    page_id = 0
    urls = set()
    headers = {'user-agent': 'Mozilla/5.0'}
    # 此处的参数为需爬取的页数
    for i in range(pages):

        url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&' \
              'logid=7115341739667250212&ipn=rj&ct=201326592&is=&fp=result&queryWord=' \
              '{0}&cl=&lm=&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&' \
              'word={1}&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&expermode=&' \
              'force=&pn={2}&rn=30&gsm=1e&1612100373755='.format(pname, pname, page_id)
        page_id += 30
        print(url)
        try:
            result = requests.get(url, headers=headers, timeout=10, allow_redirects=False)
            # urls_List = result.json()['data']
            # todo 这里有的网页解码会出错，改用.text的话要用正则表达式
            urls_List2 = result.text
            #  这里其实有可能data是空
            urls_List = json.loads(urls_List2)['data']

        except Exception as e:
            print(e.__class__.__name__)
            traceback.print_exc()
            print('网页解析错误…………,提取' + pname + "图片出错")
            continue

        for j in range(len(urls_List)):
            if urls_List[j] != {}:
                try:
                    print(j, pname + '_baidu', urls_List[j]['thumbURL'])
                    urls.add(urls_List[j]['thumbURL'])
                except Exception as e:
                    _ = e.__class__.__name__
                    # print(e.__class__.__name__)
                    traceback.print_exc()
                    continue
        # todo 这里还要看看
    # print(len(urls))
    images_urls = list(urls)
    images_names = []

    # 使用进程池-->多进程获取图片->不明白为什么不能再子进程中开子进程
    # po_baidu = Pool(process_nums)
    for k, image_url in enumerate(images_urls):
        image_name = os.path.join(save_dir, '%04d' % (k + 1) + '_'+enginee + '.jpg')
        # print(image_name)
        images_names.append(image_name)

    images_urls_names = []

    for idx in range(len(images_names)):
         images_urls_names.append((images_urls[idx], images_names[idx]))
    # print(images_urls_names)

    executor = ThreadPoolExecutor(max_workers=thread_workers)
    for _, _ in enumerate(executor.map(get_image, images_urls_names)):
        # print("task{}".format(k,))
        pass


def get_images_ulrs_from_bing(name0, pages=2, save_dir=SAVE_IMAGES_DIR, thread_workers=3):
    """
    获取bing图片每页的url
    :param pages:
    :param name0:
    :param save_dir:
    :param thread_workers:
    :return:
    """

    enginee = 'bing'
    save_dir = os.path.join(save_dir, enginee)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 用来判断哪些人已经爬取过了
    names = sorted(os.listdir(save_dir))
    if name0 in names:
        print(enginee+'_'+name0 + '_scratched')
        return None

    # 人物图片存放的路劲
    save_dir = os.path.join(save_dir, name0)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        # "User-Agent": self.ua.chrome,
        # "Connection": "close",
        'Cookie': 'MMCA=ID=72C5729F696C44CB88F81EAEEE5D20C0; '
                  'ipv6=hit=1613287263887&t=6; MUID=2520F2D5D8046C2C389EFC01D97B6D92; '
                  'MUIDB=2520F2D5D8046C2C389EFC01D97B6D92; SRCHD=AF=NOFORM; '
                  'SRCHUID=V=2&GUID=E3D012F734B14DD59EC19A994EA0C8FD&dmnchg=1; '
                  'ULC=P=3341|1:1&H=3341|1:1&T=3341|1:1; fbar=imgfbar=1; _'
                  'ITAB=STAB=TR; imgv=flts=20210214; _SS=SID=104BC94C6DA46B912EB5C6916CE76A7B&bIm=04:618; '
                  'SRCHUSR=DOB=20210129&T=1613353196000&TPC=1613353199000; ipv6=hit=1613356800070&t=4; '
                  '_EDGE_S=SID=1544C02F7428693C3010CFF07506681C&mkt=zh-cn; SRCHHPGUSR=CW=1440&CH=225&DPR=2&UTC=48'
                  '0&DM=0&HV=1613355593&WTS=63748949996&BZA=0&BRW=W&BRH=S&PLTL=686&PLTA=546&PLTN=13&SRCHLANGV2=zh-Hans'
    }

    pname = name0.split('_')[1]
    first = 1
    sfx = 1
    count = 0
    image_urls = []
    next_html_urls = []
    # key = urllib.parse.quote(pname)
    orig_url = 'https://cn.bing.com/images/async?q={0}&first=1&count=35&relp=35&' \
               'tsc=ImageBasicHover&datsrc=I&layout=ColumnBased&mmasync=1&dgState=' \
               'c*6_y*1485s1597s1396s1378s1548s1433_i*36_w*182&' \
               'IG=36E7E97B4D9D4E66A8E101D22A22E6C2&SFX=1&iid=images.5533'.format(pname, )

    prefix = 'https://cn.bing.com'
    page_nums = len(next_html_urls)

    while sfx < pages:
    # while True:
        try:
            # requests.DEFAULT_RETRIES = 15
            html_data = requests.get(orig_url, headers=headers, timeout=10, allow_redirects=False).text
            # print('orig',orig_url)
            # html_data = sess1.get(orig_url, headers=self.headers, timeout=10,
            #                       allow_redirects=False, verify=False).text
        except Exception as e:
            print(orig_url, '网页无法访问…………,')
            print(e.__class__.__name__)
            traceback.print_exc()
            continue

        page_data = etree.HTML(html_data)
        try:
            tmp = page_data.xpath('//div/@data-nexturl')[0]
            next_url = prefix + tmp
            if next_url == prefix:
                print(pname, '网页已经爬取完……')
                break
            # 获取下一页的url
            sfx += 1
            orig_url = next_url + '22BE8B13C2D345A3B3807486F83BF32E&SFX={}&iid=images.5543'.format(sfx)
            # print('origurl',orig_url)
            next_html_urls.append(next_url)
            page_nums += 1
            count += 35
        except Exception as e:
            print(e.__class__.__name__)
            traceback.print_exc()
            print('网页无法访问…………,')
            continue

    # 取出页数
    for url in next_html_urls:
        try:
            # requests.DEFAULT_RETRIES = 15

            html_data = requests.get(url, headers=headers, timeout=10, allow_redirects=False).text
            # html_data = sess.get(url, headers=self.headers, timeout=10, allow_redirects=False, verify=False).text
            page_data = etree.HTML(html_data)
            # 缩略图url
            # images_urls = page_data.xpath('//div[@class="img_cont hoff"]/img/@src')
            # image_urls.extend(images_urls)
            # 原始图url
            images_urls = page_data.xpath('//div[@class="imgpt"]/a[@class="iusc"]/@m')

        except Exception as e:
            print(e.__class__.__name__)
            print('网页解析错误…………,提取' + pname + "图片出错")
            traceback.print_exc()
            continue

        for k,murl in enumerate(images_urls):
            try:
                img_url = json.loads(murl)
            except Exception as e:
                print(e.__class__.__name__)
                traceback.print_exc()
                print('网页json解析错误…………,提取' + pname + "图片出错")
                continue
            print(k, pname+'_bing', img_url['murl'])
            image_urls.append(img_url['murl'])

    image_urls = list(set(image_urls))

    n = len(image_urls)
    images_names = []

    # 使用进程池-->多进程获取图片

    for k, image_url in enumerate(image_urls):
        image_name = os.path.join(save_dir, '%04d' % (k + 1) + '_' + enginee + '.jpg')
        print(image_name)
        images_names.append(image_name)

    images_urls_names = []

    for idx in range(len(images_names)):
        images_urls_names.append((image_urls[idx], images_names[idx]))
    # print(images_urls_names)
    executor = ThreadPoolExecutor(max_workers=thread_workers)
    for _, _ in enumerate(executor.map(get_image, images_urls_names)):
        pass


def get_images_ulrs_from_sougou(name0, total_img=48, save_dir=SAVE_IMAGES_DIR, thread_workers=3):
    """
    获取搜狗图片url
    :param thread_workers:
    :param name0:
    :param save_dir:
    :param total_img:
    :return:
    """

    enginee = 'sougou'
    save_dir = os.path.join(save_dir, enginee)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    names = sorted(os.listdir(save_dir))
    if name0 in names:
        print(enginee+'_'+name0 + '_scratched')
        return None

    # 人物图片存放的路径
    save_dir = os.path.join(save_dir, name0)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    headers = {'user-agent': 'Mozilla/5.0'}

    pname = name0.split('_')[1]
    mod = total_img % 48
    if mod == 0.0:
        pages_num = total_img // 48
    else:
        pages_num = total_img // 48 + 1

    # 用来存图片url
    images_urls = []
    for i in range(pages_num):

        url = 'https://pic.sogou.com/napi/pc/searchList?mode=1&' \
              'start={}&xml_len=48&query={}'.format(i * 48, pname)

        try:
            imgs = requests.get(url, headers=headers, timeout=10, allow_redirects=False)

        except Exception as e:
            print(e.__class__.__name__)
            print(traceback.print_exc())
            print(url, 'sougou网页访问错误……')
            continue
        try:
            # jd = json.loads(imgs.text)
            jd = imgs.json()['data']
        except Exception as e:
            print(e.__class__.__name__)
            print(traceback.print_exc())
            print('sougou网页解析错误……')
            continue

        jd = jd['items']
        for k, pic_url in enumerate(jd):
            print(k, pname + '_sougou', pic_url['oriPicUrl'])
            images_urls.append(pic_url['oriPicUrl'])

    images_names = []
    for k, image_url in enumerate(images_urls):
        image_name = os.path.join(save_dir, '%04d' % (k + 1) + '_' + enginee + '.jpg')
        # print(image_name)
        images_names.append(image_name)

    images_urls_names = []
    for idx in range(len(images_names)):
         images_urls_names.append((images_urls[idx], images_names[idx]))
    # print(images_urls_names)
    # 使用多线程
    executor = ThreadPoolExecutor(max_workers=thread_workers)
    for _, _ in enumerate(executor.map(get_image, images_urls_names)):
        # print("task{}".format(k,))
        pass


def get_images_ulrs(args):
    """
    :param args:
    :return:
    """
    enginee = args[0]
    txt_path = args[1]
    save_dir = args[2]

    thread_workers = args[3]
    name_list = get_names(txt_path)

    # 使用多线程的话，可能访问太快，有的图片获取不到
    # 还需要修改图片保存路径，则修改全局变量SAVE_IMAGE_DIR
    if thread_workers > 1:

        print('sassa--------------', SAVE_IMAGES_DIR)
        if enginee == 'baidu':
            print('baidu')
            executor_baidu = ThreadPoolExecutor(max_workers=3)
            for _, _ in enumerate(executor_baidu.map(get_images_ulrs_from_baidu, name_list)):
                pass
        if enginee == 'bing':
            print('bing')
            executor_baidu = ThreadPoolExecutor(max_workers=3)
            for _, _ in enumerate(executor_baidu.map(get_images_ulrs_from_bing, name_list)):
                pass
        if enginee == 'sougou':
            print('sougou')
            executor_baidu = ThreadPoolExecutor(max_workers=3)
            for _, _ in enumerate(executor_baidu.map(get_images_ulrs_from_sougou, name_list)):
                pass
    # 使用单线程
    if thread_workers <= 1:
        for name in name_list:
            if enginee == 'baidu':
                print('baidu')
                get_images_ulrs_from_baidu(name0=name, save_dir=save_dir,)
            if enginee == 'bing':
                print('bing')
                get_images_ulrs_from_bing(name0=name, save_dir=save_dir,)
            if enginee == 'sougou':
                print('sougou')
                get_images_ulrs_from_sougou(name0=name, save_dir=save_dir,)


if __name__ == '__main__':
    txtfile_path = './txt/Chines_celebrity_names_v1.txt'
    save_image_dir = './images3'
    arguments = []
    th_workers = 1
    # 这里选择用哪个搜索引擎爬取图片
    engines = ['baidu', 'bing', 'sougou']
    for engine in engines:
        arguments.append((engine, txtfile_path, save_image_dir, th_workers))

    po = Pool(3)
    po.map_async(get_images_ulrs, arguments)
    po.close()
    po.join()

