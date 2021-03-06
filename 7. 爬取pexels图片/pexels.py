# -*- coding: utf-8 -*-
# 2018/4/7 20:55
# 根据输入的内容爬取pexels的图片，使用了谷歌翻译
# googletrans:  https://github.com/ssut/py-googletrans

import requests
from lxml import etree
from googletrans import Translator
import os
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36',
}
path = os.path.expanduser('~') + '\\Desktop\\pic\\'


# 输入的中文翻译后会生成的词会成为目录，相应的图片会放入其中
def save_photo(trans, src):
    data = requests.get(src, headers=headers)
    if os.path.exists(path + trans + '\\'):
        pass
    else:
        os.mkdir(path + trans + '\\')
    fp = open(path + trans + '\\' + src[src.rindex('/') + 1:src.index('?')], 'wb')
    fp.write(data.content)
    fp.close()


if __name__ == '__main__':
    translator = Translator(service_urls=['translate.google.cn', 'translate.google.com'])
    while True:
        search_content = input('要下载的图片(输入“exit”退出):')
        if search_content.lower() == 'exit':
            break
        else:
            translate_content = translator.translate(search_content, 'en').text
            print(translate_content)
            url = 'https://www.pexels.com/search/' + translate_content + '/'
            res = requests.get(url, headers=headers)
            selector = etree.HTML(res.text)
            imgs = selector.xpath('//img[@class="photo-item__img"]/@src')
            for img in imgs:
                # 网速越快，图片保存的速度也越快
                save_photo(translate_content, img)
                time.sleep(1)
