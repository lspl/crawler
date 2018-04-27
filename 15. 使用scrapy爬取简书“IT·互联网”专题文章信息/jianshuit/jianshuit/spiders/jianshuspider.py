# -*- coding: utf-8 -*-
# 2018/4/27 20:36

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from jianshuit.items import JianshuitItem


class jianshuit(CrawlSpider):
    name = 'jianshuit'
    start_urls = ['https://www.jianshu.com/c/V2CqjW?order_by=added_at&page=1']

    def parse(self, response):
        item = JianshuitItem()
        selector = Selector(response)
        infos = selector.xpath('//ul[@class="note-list"]/li')
        for info in infos:
            user = info.xpath('div[1]/div[1]/div[1]/a[1]/text()').extract()[0]
            time = info.xpath('div[1]/div[1]/div[1]/span/@data-shared-at').extract()[0].replace('T', ' ').replace('+', ' ')
            title = view = comment = like = reward = '0'
            try:
                title = info.xpath('div[1]/a[1]/text()').extract()[0]
            except IndexError:
                pass
            try:
                view = info.xpath('div[1]/div[2]/a[1]/text()').extract()[1].strip()
            except IndexError:
                pass
            try:
                comment = info.xpath('div[1]/div[2]/a[2]/text()').extract()[1].strip()
            except IndexError:
                pass
            try:
                like = info.xpath('div[1]/div[2]/span[1]/text()').extract()[0]
            except IndexError:
                pass
            try:
                reward = info.xpath('div[1]/div[2]/span[2]/text()').extract()[0]
            except IndexError:
                pass
            item['user'] = user
            item['time'] = time
            item['title'] = title
            item['view'] = view
            item['comment'] = comment
            item['like'] = like
            item['reward'] = reward
            yield item
        urls = ['https://www.jianshu.com/c/V2CqjW?order_by=added_at&page={}'.format(str(i)) for i in range(2, 101)]
        for url in urls:
            yield Request(url, callback=self.parse)


