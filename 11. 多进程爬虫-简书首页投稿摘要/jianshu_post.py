# -*- coding: utf-8 -*-
# 2018/4/10 21:40
# 爬取简书网“首页投稿”的内容，使用多进程，存入mongo数据库中。包括：作者，时间，标题，摘要，查看数，评论数，喜欢数，打赏数
'''
多进程运行参考时间：117s
单进程爬虫被封ip了，多进程爬虫没事。
内容加载为异步方式，也就是逆向工程的方法。链接的获取可以看书或参考：https://www.jianshu.com/p/cb7207038bd1
PS: 虽然简书的首页投稿即将下线，但是作为对爬虫限制不强的网站之一，还是非常不错的
'''


import requests
import pymongo
import time
from lxml import etree
from multiprocessing import Pool


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36',
}
client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
jianshu_post = mydb['jianshu_post']


def get_jianshu_info(url):
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    infos = selector.xpath('//div[@class="content"]')
    for info in infos:
        author = info.xpath('div/div/a/text()')[0]
        time0 = info.xpath('div/div/span/@data-shared-at')[0].replace('T', ' ').replace('+08:00', '')
        title = info.xpath('a/text()')[0]
        content = info.xpath('p/text()')[0].strip()
        views = info.xpath('div[2]/a[1]/text()')[1].strip()
        # 有些没有评论链接和数字
        try:
            comments = info.xpath('div[2]/a[2]/text()')[1].strip()
        except IndexError:
            comments = 0
        t = 0
        try:
            if info.xpath('div[2]/span/text()')[1].strip() == '付费':
                t = 1
        except IndexError:
            pass
        likes = info.xpath('div[2]/span[' + str(1 + t) + ']/text()')[0]
        try:
            rewards = info.xpath('div[2]/span[' + str(2 + t) + ']/text()')[0]
        except IndexError:
            rewards = 0
        data = {'author': author, 'time': time0, 'title': title, 'content': content, 'views': views, 'comments': comments, 'likes': likes, 'rewards': rewards}
        jianshu_post.insert_one(data)


if __name__ == '__main__':
    t1 = time.time()
    urls = ['https://www.jianshu.com/c/bDHhpK?order_by=added_at&page={}'.format(str(i)) for i in range(0, 1000)]
    pool = Pool(processes=4)
    pool.map(get_jianshu_info, urls)
    t2 = time.time()
    print('total time', t2 - t1)
