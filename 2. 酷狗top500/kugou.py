# -*- coding: utf-8 -*-
# 2018/3/25 21:46
# 爬取酷狗top500信息： http://www.kugou.com/yy/rank/home/1-8888.html?from=rank
# CSS selector 由 chrome得到
# 爬虫获取的数据保存在和当前文件同一目录的temp.txt中

import os
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}
f = open(os.path.abspath('.') + '\\temp.txt', 'a', encoding='utf-8')


def get_info(url0):
    res = requests.get(url0, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    ranks = soup.select('#rankWrap > div.pc_temp_songlist > ul > li > span.pc_temp_num')
    titles = soup.select('#rankWrap > div.pc_temp_songlist > ul > li > a')
    times = soup.select('#rankWrap > div.pc_temp_songlist > ul > li > span.pc_temp_tips_r > span')
    for rank, title, time0 in zip(ranks, titles, times):
        infos = title.get_text().split('-')
        data = {
            'rank': rank.get_text().strip(),
            'song': infos[1].strip(),
            'singer': infos[0].strip(),
            'time': time0.get_text().strip()
        }
        f.write(str(data) + '\n')


if __name__ == '__main__':
    f0 = open(os.path.abspath('.') + '\\temp.txt', 'w')
    f0.truncate()
    f0.close()
    urls = ['http://www.kugou.com/yy/rank/home/{}-8888.html'.format(str(i)) for i in range(1, 24)]
    for url in urls:
        get_info(url)
    f.close()
