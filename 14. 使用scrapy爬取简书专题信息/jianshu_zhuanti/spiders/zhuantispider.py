# -*- coding: utf-8 -*-
# 2018/4/25 17:03

import re
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from jianshu_zhuanti.items import JianshuZhuantiItem


class jianshu_zhuanti(CrawlSpider):
    name = 'jianshu_zhuanti'
    start_urls = ['https://www.jianshu.com/recommendations/collections?page=1&order_by=hot']

    def parse(self, response):
        item = JianshuZhuantiItem()
        selector = Selector(response)
        infos = selector.xpath('//div[@class="collection-wrap"]')
        for info in infos:
            name = info.xpath('a[1]/h4/text()').extract()[0]
            introduction = ''
            # 极少数专题介绍为空
            try:
                introduction = info.xpath('a[1]/p/text()').extract()[0].replace('\r', '').replace('\n', ' ')
            except IndexError:
                pass
            article_number = re.findall('.*?(\d+).*?', info.xpath('div[1]/a/text()').extract()[0], re.S)[0]
            fans = info.xpath('div[1]/text()').extract()[0].replace(' · ', '').replace('人关注', '')

            print(name, introduction, article_number, fans)
            item['name'] = name
            item['introduction'] = introduction
            item['article_number'] = article_number
            item['fans'] = fans

            yield item

        urls = ['https://www.jianshu.com/recommendations/collections?page={}&order_by=hot'.format(str(i)) for i in range(2, 38)]
        for url in urls:
            yield Request(url, callback=self.parse)
