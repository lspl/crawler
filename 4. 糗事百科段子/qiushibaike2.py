# -*- coding: utf-8 -*-
# 2018/4/3 21:06
# 测试正则表达式，BeautifulSoup, Lxm的运行速度（33秒左右，不知道书上为啥那么快。。）

import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}


def re_scrapper(url):
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    ids = re.findall('<h2>(.*?)</h2>', res.text, re.S)
    contents = re.findall('<div class="content">.*?<span>(.*?)</span>.*?</div>', res.text, re.S)
    laughs = re.findall('<i class="number">(\d+)</i> 好笑', res.text, re.S)
    comments = re.findall('<i class="number">(\d+)</i> 评论', res.text, re.S)
    for id0, content, laugh, comment in zip(ids, contents, laughs, comments):
        info = {
            'id': id0.strip(),
            'content': content.strip().replace('<br/>', '\n'),
            'laugh': laugh,
            'comment': comment
        }


def bs_scrapper(url0):
    res = requests.get(url0, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    ids = soup.select('a > h2')
    contents = soup.select("a > div.content > span")  # 注意写法
    laughs = soup.select('span.stats-vote > i')
    comments = soup.select('span.stats-comments > a > i')
    for id0, content, laugh, comment in zip(ids, contents, laughs, comments):
        info = {
            'id': id0.get_text().strip(),
            'content': content.get_text().strip(),
            'laugh': laugh.get_text(),
            'comment': comment.get_text()
        }


def lxml_scrapper(url0):
    res = requests.get(url0, headers=headers)
    res.encoding = 'utf-8'
    selector = etree.HTML(res.text)
    url_infos = selector.xpath('//div[starts-with(@class, "article block untagged mb15 typs_")]')
    for url_info in url_infos:
        info = {
            'id': url_info.xpath('div[1]/a[2]/h2/text() | div[1]/span[2]/h2/text()')[0].strip(),
            'content': url_info.xpath('a[1]/div/span/text()')[0].strip(),
            'laugh': url_info.xpath('div[2]/span[1]/i/text()')[0].strip(),
            'comment': url_info.xpath('div[2]/span[2]/a/i/text()')[0].strip()
        }


if __name__ == '__main__':
    urls = urls = ['https://www.qiushibaike.com/text/page/{}/'.format(str(i)) for i in range(1, 14)]
    for name, scrapper in [('Regular expressions', re_scrapper), ('BeautifulSoup', bs_scrapper),
                           ('Lxml', lxml_scrapper)]:
        start = time.time()
        for url in urls:
            scrapper(url)
        end = time.time()
        print(name, end - start)
