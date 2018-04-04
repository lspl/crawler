# -*- coding: utf-8 -*-
# 2018/3/28 20:58
# 爬取糗事百科: https://www.qiushibaike.com/text/
# 爬虫获取的数据保存在和当前文件同一目录的temp.txt中

'''
    PS: 书上给的代码有误，因为匿名用户的存在（有兴趣的可以用书上的代码运行一下，再和网页的结果匹配下）
    匿名用户应该是没有性别和等级的，但是仔细看源文件，会发现匿名用户后有注释掉的性别和等级(应该是假的，性别都是男，
年龄都是32)
'''

import re
import os
import time
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}


def judge(sex):
    if sex == 'man':
        return '男'
    return '女'


def get_info(url0, f1):
    res = requests.get(url0, headers=headers)
    infos = re.findall('<a href="/users/(.*?)/" .*? rel="nofollow"', res.text)
    sexs = re.findall('<div class="articleGender (.*?)Icon">.*?</div>.*', res.text)
    levels = re.findall('<div class="articleGender \D+Icon">(.*?)</div>', res.text)
    names = re.findall('<h2>(.*?)</h2>', res.text, re.S)
    contents = re.findall('<div class="content">.*?<span>(.*?)</span>.*?</div>', res.text, re.S)
    laughs = re.findall('<span class="stats-vote"><i class="number">(\d+)</i>', res.text, re.S)
    comments = re.findall('<span class="stats-comments">.*?<i class="number">(\d+)</i>', res.text, re.S)
    for info, name, sex, level, content, laugh, comment in zip(infos, names, sexs, levels, contents, laughs, comments):
        if name == '匿名用户':
            f1.write(name + '\n' + content.strip().replace('<br/>', '\n') + '\n' + laugh + '\t' + comment + '\n\n')
        else:
            f1.write('https://www.qiushibaike.com/users/' + info + '/\n' + name.strip() + '\t' + judge(
                sex) + '\t' + level + '\n' + content.strip().replace('<br/>',
                                                                     '\n') + '\n' + laugh + '\t' + comment + '\n\n')


if __name__ == '__main__':
    f0 = open(os.path.abspath('.') + '\\temp.txt', 'w')
    f0.truncate()
    f0.close()
    f = open(os.path.abspath('.') + '\\temp.txt', 'a', encoding='utf-8')
    urls = ['https://www.qiushibaike.com/text/page/{}/'.format(str(i)) for i in range(1, 14)]
    for url in urls:
        get_info(url, f)
        time.sleep(1)
    f.close()
