# -*- coding: utf-8 -*-
# 2018/3/26 20:34
# 爬取斗破苍穹小说全文：http://www.doupoxs.com/doupocangqiong/
# CSS selector由firefox复制得到
# 爬虫获取的数据保存在和当前文件同一目录的result.txt中


'''
PS:
    temp.txt用于保存爬虫的初始文件，由于初始文件有许多妨碍阅读的部分，因此
需要进行过滤，最终的结果保存在result.txt中(15M)，并且临时文件temp.txt会被
删掉。可以直接当小说看。比如用手机UC浏览器打开，章节会自动分好，非常方便。
    为了防止爬虫挂掉，每爬一章就休息一秒（亲测，不休眠会挂。）。并且在控制台
打印当前爬虫进度。
'''

import os
import time
import requests
from bs4 import BeautifulSoup

old_file = os.path.abspath('') + '\\temp.txt'
new_file = os.path.abspath('') + '\\result.txt'
f = open(old_file, 'w', encoding='utf-8')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}


def get_info(url0):
    res = requests.get(url0, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    if res.status_code == 200:
        title = soup.select('.read_chapterName > h1')
        content = soup.select('.read_chapterDetail')
        f.write(title[0].get_text() + '\n' + str(content[0]).replace('<p>', '  ').replace('</p>', '\n') + '\n')
        print('正在爬取: ' + title[0].get_text())


if __name__ == '__main__':
    urls = ['http://www.doupoxs.com/doupocangqiong/{}.html'.format(str(i)) for i in range(1, 1666)]
    for url in urls:
        get_info(url)
        time.sleep(1)
    f.close()

    oldFile = open(old_file, 'r', encoding='utf-8')
    newFile = open(new_file, 'w')
    newFile.truncate()
    newFile.close()
    newFile = open(new_file, 'a', encoding='utf-8')
    for line in oldFile.readlines():
        if line.startswith('<div') or line.startswith('</div') or line.startswith('<a class') or len(line) == 1:
            pass
        else:
            newFile.write(line + '\n')
    oldFile.close()
    newFile.close()
    os.remove(old_file)
