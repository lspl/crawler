# -*- coding: utf-8 -*-
# 2018/4/8 19:49
# 获取糗事百科网用户地址信息
# 程序运行时间参考：4606s
# excel数据透视图的分类计数可以参考 https://jingyan.baidu.com/article/359911f5b15b5457ff030650.html

import requests
from lxml import etree
import time
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36',
}
fp = open('map.csv', 'w+', newline='', encoding='utf-8')
writer = csv.writer(fp)
writer.writerow(('address', 'longitude', 'latitude'))


def get_user_address(url1):
    res1 = requests.get(url1, headers=headers)
    selector1 = etree.HTML(res1.text)
    city = selector1.xpath('//div[@class="user-col-left"]/div[2]/ul/li[4]/text()')
    if len(city) > 0 and city[0] != '未知':
        try:
            province = city[0][:city[0].index(' ·')]
        except ValueError:
            province = ''
        if province != '国外' and province != '未知':
            while True:
                url2 = 'http://api.map.baidu.com/geocoder?output=json&key=f247cdb592eb43ebac6ccd27f796e2d2&address=' + province
                answer = requests.get(url2, headers=headers).json()
                try:
                    t = len(answer['result'])
                    break
                except KeyError:
                    pass
            if t > 0:
                lon = float(answer['result']['location']['lng'])
                lat = float(answer['result']['location']['lat'])
                writer.writerow((province, lon, lat))


if __name__ == '__main__':
    t1 = time.time()
    urls1 = ['https://www.qiushibaike.com/8hr/page/{}/'.format(str(i)) for i in range(1, 14)]
    urls2 = ['https://www.qiushibaike.com/hot/page/{}/'.format(str(i)) for i in range(1, 14)]
    urls3 = ['https://www.qiushibaike.com/imgrank/page/{}/'.format(str(i)) for i in range(1, 14)]
    urls4 = ['https://www.qiushibaike.com/text/page/{}/'.format(str(i)) for i in range(1, 14)]
    urls5 = ['https://www.qiushibaike.com/history/ad796836d306b57deaedc74b2d805fe7/page/{}/'.format(str(i)) for i in range(1, 21)]
    urls6 = ['https://www.qiushibaike.com/pic/page/{}/'.format(str(i)) for i in range(1, 36)]
    urls7 = ['https://www.qiushibaike.com/textnew/page/{}/'.format(str(i)) for i in range(1, 36)]
    urls = urls1 + urls2 + urls3 + urls4 + urls5 + urls6 + urls7
    for i in range(0, len(urls)):
        res = requests.get(urls[i], headers=headers)
        selector = etree.HTML(res.text)
        users = selector.xpath('//div[@class="author clearfix"]')
        for user in users:
            href = user.xpath('a[2]/@href')
            if len(href) > 0:
                get_user_address('https://www.qiushibaike.com' + href[0])
        print(i)
        time.sleep(1)
    fp.close()
    t2 = time.time()
    print('total time:', t2 - t1)