# -*- coding: utf-8 -*-
# 2018/4/4 13:55
# 爬取豆瓣top250的书籍信息
# 得到的temp.csv直接用excel打开会乱码（用记事本打开不乱码），可以用记事本打开，另存为utf-8，再用excel打开即可

import csv
import re
import os
import requests
import time
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}

if __name__ == '__main__':
    fp = open(os.path.abspath('.') + "\\temp.csv", 'w+', encoding='utf-8', newline='')
    writer = csv.writer(fp)
    writer.writerow(('name', 'url', 'original_name', 'country', 'author', 'translator', 'publisher', 'date', 'price',
                     'rate', 'comments', 'review'))

    urls = ['https://book.douban.com/top250?start={}'.format(str(i * 25)) for i in range(0, 10)]
    for url0 in urls:
        res = requests.get(url0, headers=headers)
        res.encoding = 'utf-8'
        selector = etree.HTML(res.text)
        infos = selector.xpath('//tr[@class="item"]')
        for info in infos:
            name = info.xpath('td[2]/div/a/text()')[0].strip()
            url = info.xpath('td/a/@href')[0]
            original_name = ''
            # 如果不加异常，则当书籍的原名不是中文时，评分会覆盖掉原名
            try:
                original_name = info.xpath('td[2]/div[1]/span/text()')[0]
            except IndexError:
                pass
            concrete = info.xpath('td[2]/p/text()')[0].strip().split('/')
            author_info = concrete[0].strip().split(' ')
            if len(author_info) == 1:
                country = '中国'
                author = author_info[0]
            else:
                country = author_info[0].replace('[', '').replace(']', '')
                if country == '清':
                    country = '中国 清'
                author = author_info[1]
            if len(concrete) == 5:
                translator = concrete[1]
                publisher = concrete[2]
                date = concrete[3]
                price = concrete[4]
            else:
                translator = ''
                publisher = concrete[1]
                date = concrete[2]
                price = concrete[3]
            rate = info.xpath('td[2]/div[2]/span[2]/text()')[0]
            comments = re.match('.*?(\d+).*?', info.xpath('td[2]/div[2]/span[3]/text()')[0].strip().replace('(', '').replace(')', '').replace('\n', '').replace(' ', '')).group(1)
            # 有些书没有review
            review = ''
            try:
                review = info.xpath('td[2]/p[2]/span/text()')[0].strip()
            except IndexError:
                pass
            writer.writerow(
                (name, url, original_name, country, author, translator, publisher, date, price, rate, comments, review))
        time.sleep(1)
    fp.close()
