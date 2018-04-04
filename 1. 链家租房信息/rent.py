# -*- coding: utf-8 -*-
# 2018/3/25 17:03
# 爬取租房信息 https://bj.lianjia.com/zufang/rs%E7%9F%B3%E9%97%A8/
# CSS selector的信息来自chrome
# 爬虫获取的数据保存在和当前文件同一目录的temp.txt中

import os
import requests
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}
# os.path.abspath('.')用于获取当前文件所在的目录
f = open(os.path.abspath('.') + '\\temp.txt', 'w', encoding='utf-8')


def get_info(url0):
    res = requests.get(url0, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    images = soup.select('#house-lst > li > div.pic-panel > a > img')
    titles = soup.select('#house-lst > li > div.info-panel > h2 > a')
    positions = soup.select('#house-lst > li > div.info-panel > div.col-1 > div.where > a > span')
    types = soup.select('#house-lst > li > div.info-panel > div.col-1 > div.where > span.zone > span')
    squares = soup.select('#house-lst > li > div.info-panel > div.col-1 > div.where > span.meters')
    directions = soup.select(
        '#house-lst > li > div.info-panel > div.col-1 > div.where > span')
    prices = soup.select('#house-lst > li > div.info-panel > div.col-3 > div.price > span')
    visitors = soup.select('#house-lst > li > div.info-panel > div.col-2 > div > div > span')
    for image, title, position, type0, square, direction, price, visitor in \
            zip(images, titles, positions, types, squares, directions, prices, visitors):
        data = {'image': image.get("data-img"),
                'title': title.get_text().strip(),
                'position': position.get_text().strip(),
                'type': type0.get_text().strip(),
                'square': square.get_text().strip(),
                'direction': direction.get_text().strip(),
                'price': price.get_text().strip(),
                'visitor': visitor.get_text().strip()}
        f.write(str(data) + '\n')


if __name__ == '__main__':
    urls = ['https://bj.lianjia.com/zufang/rs%E7%9F%B3%E9%97%A8/',
            'https://bj.lianjia.com/zufang/pg2rs%E7%9F%B3%E9%97%A8/',
            'https://bj.lianjia.com/zufang/pg3rs%E7%9F%B3%E9%97%A8/',
            'https://bj.lianjia.com/zufang/pg4rs%E7%9F%B3%E9%97%A8/']
    for url in urls:
        get_info(url)
        time.sleep(1)
