# -*- coding: utf-8 -*-
# 2018/4/12 17:12
# 爬取简书网七日热门信息(https://www.jianshu.com/trending/weekly),写入mongodb数据中
# 爬取文章详情页：作者ID、文章名、发布日期、字数、阅读、评论、喜欢、赞赏数量、收录专题
'''
    七日热门模块异步加载的内容加载和之前的重复，不知道是不是bug. 所以并不需要多个url
    多进程：103s; 单进程：76s. 还没明白为什么
'''

import requests
import pymongo
import re
import json
import time
from lxml import etree
from multiprocessing import Pool


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
}
client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
jianshu_weekly = mydb['jianshu_weekly']


def get_url(url):
    hrefs = etree.HTML(requests.get(url, headers=headers).text).xpath('//a[@class="title"]/@href')
    for href in hrefs:
        res = requests.get('https://www.jianshu.com' + href, headers=headers)
        selector = etree.HTML(res.text)
        id = selector.xpath('//span[@class="name"]/a/text()')[0]
        title = selector.xpath('//h1[@class="title"]/text()')[0]
        publish_time = selector.xpath('//span[@class="publish-time"]/text()')[0]
        word_count = selector.xpath('//span[@class="wordage"]/text()')[0].split(' ')[1]
        view_count = re.findall('"views_count":(.*?),', res.text, re.S)[0]
        comment_count = re.findall('"comments_count":(.*?),', res.text, re.S)[0]
        like_count = re.findall('"likes_count":(.*?),', res.text, re.S)[0]
        reward_count = re.findall('"total_rewards_count":(.*?),', res.text, re.S)[0]
        note_id = selector.xpath('//div[@data-vcomp="recommended-notes"]/@data-note-id')[0]
        topics = list()
        include_urls = ['https://www.jianshu.com/notes/{}/included_collections?page={}'.format(note_id, str(i)) for i in range(1, 11)]
        for include_url in include_urls:
            html = requests.get(include_url, headers=headers)
            json_data = json.loads(html.text)
            includes = json_data['collections']
            if len(includes) == 0:
                pass
            else:
                for include in includes:
                    include_title = include['title']
                    topics.append(include_title)
        data = {
            'id': id, 'title': title, 'publish_time': publish_time, 'word_count': word_count,
            'view_count': view_count, 'comment_count': comment_count, 'like_count': like_count,
            'reward_count': reward_count, 'topics': topics,
        }
        jianshu_weekly.insert_one(data)


if __name__ == '__main__':
    t1 = time.time()
    url = ['https://www.jianshu.com/trending/weekly']
    pool = Pool(processes=4)
    pool.map(get_url, url)
    # get_url(url[0])
    t2 = time.time()
    print('total time:', t2 - t1)
