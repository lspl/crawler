# -*- coding: utf-8 -*-
# 2018/4/10 18:22
# 爬取豆瓣电影top250的信息，并写入mysql数据库中。包括：电影名称，导演，主角，类型，制片国家，上映时间，片长和评分

'''
    程序运行参考时间：311s
    注意：有些电影的详情页不存在，如https://movie.douban.com/subject/5912992/
    另外：演员，主角，类型，制片国家，上映时间，片长 都可能有多个
    数据库和表创建语句：
    create database mydb;
    use mydb;
    create table doubanmovie(name TEXT, director TEXT, actor TEXT, style TEXT, country TEXT,
            release_time TEXT, time TEXT, score TEXT)engine innodb default charset=utf8;
'''

import requests
import re
import time
import pymysql.cursors

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
}
conn = pymysql.connect(host='localhost', user='root', passwd='', db='mydb', port=3306, charset='utf8')
cursor = conn.cursor()


def get_info(url):
    hrefs = re.findall('<div class="hd">.*?<a href="(.*?)" class="">', requests.get(url, headers=headers).text, re.S)
    for href in hrefs:
        res = requests.get(href, headers=headers)
        if res.status_code == 200:  # 有些电影详情页不存在，如 https://movie.douban.com/subject/5912992/
            name = re.findall('<span property="v:itemreviewed">(.*?)</span>', res.text, re.S)[0].replace('&#39;', '\'')
            director = re.findall('rel="v:directedBy">(.*?)</a>', res.text, re.S)[0]
            actor_all = re.findall('rel="v:starring">(.*?)</a>', res.text, re.S)
            actors = ''
            for actor in actor_all:
                actors = actors + actor + ' '
            actors = actors.strip()
            style_all = re.findall('property="v:genre">(.*?)</span>', res.text, re.S)
            style = ''
            for style0 in style_all:
                style = style + ' / ' + style0
            style = style[3:]
            country = re.findall('<span class="pl">制片国家/地区:</span> (.*?)<br/>', res.text, re.S)[0]
            release_time_all = re.findall('property="v:initialReleaseDate" content=".*?">(.*?)</span>', res.text, re.S)
            release_time = ''
            for t1 in release_time_all:
                release_time = release_time + t1 + ' / '
            release_time = release_time[:-3]
            time0 = re.findall('<span property="v:runtime" content=".*?">(.*?)<br/>', res.text, re.S)[0].replace(
                '</span>', '')
            score = re.findall('<strong class="ll rating_num" property="v:average">(.*?)</strong>', res.text, re.S)[0]
            cursor.execute(
                "insert into doubanmovie (name, director, actor, style, country, release_time, time, score) values(%s, %s, %s, %s, %s, %s, %s, %s)",
                (name, director, actors, style, country, release_time, time0, score))
    conn.commit()


if __name__ == '__main__':
    t1 = time.time()
    urls = ['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0, 250, 25)]
    for i in range(0, len(urls)):
        get_info(urls[i])
        print(i * 25)
        time.sleep(1)
    t2 = time.time()
    print('total time:', t2 - t1)
