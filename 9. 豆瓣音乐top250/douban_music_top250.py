# -*- coding: utf-8 -*-
# 2018/4/10 9:03
# 爬取豆瓣音乐top250的数据，包括：歌名，表演者，流派，发行时间，出版者和评分
# 运行参考时间：412s

import requests
import pymongo
import time
import re

client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
musictop = mydb['musictop']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36',
}


def get_url(url):
    t = requests.get(url, headers=headers).text
    hrefs = re.findall('<a class="nbg" href="(.*?)"', t, re.S)
    for href in hrefs:
        res = requests.get(href, headers=headers)
        name = re.findall('<div id="wrapper">.*?<h1>.*?<span>(.*?)</span>', res.text, re.S)[0]
        author = re.findall('表演者:.*?>(.*?)</a>', res.text, re.S)[0]
        try:
            type0 = re.findall('<span class="pl">流派:</span>&nbsp;(.*?)<br />', res.text, re.S)[0].strip()
        except IndexError:
            type0 = ''  # 没有流派 参考 https://music.douban.com/subject/6064884/
        publish_time = re.findall('<span class="pl">发行时间:</span>&nbsp;(.*?)<br />', res.text, re.S)[0].strip()
        try:
            publisher = re.findall('<span class="pl">出版者:</span>&nbsp;(.*?)<br />', res.text, re.S)[0].strip()
        except IndexError:
            publisher = ''  # 没有出版者 参考 https://music.douban.com/subject/4060882/
        score = re.findall('<strong class="ll rating_num" property="v:average">(.*?)</strong>', res.text)[0]
        info = {'name': name, 'author': author, 'type': type0, 'publish_time': publish_time, 'publisher': publisher, 'socre': score}
        musictop.insert_one(info)


if __name__ == '__main__':
    urls = ['https://music.douban.com/top250?start={}'.format(str(i)) for i in range(0, 250, 25)]
    t1 = time.time()
    for i in range(0, len(urls)):
        get_url(urls[i])
        print(i * 25)
        time.sleep(1)
    t2 = time.time()
    print('total time:', t2 - t1)
