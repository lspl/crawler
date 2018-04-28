# -*- coding: utf-8 -*-
# 2018/4/28 14:32

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from jianshu_author.items import JianshuAuthorItem


# 跨页面爬虫时注意参数的传递方式
class author(CrawlSpider):
    name = 'jianshu_author'
    start_urls = ['https://www.jianshu.com/recommendations/users?page=1']

    def parse(self, response):
        base_url = 'https://www.jianshu.com'
        selector = Selector(response)
        infos = selector.xpath('//div[@class="wrap"]')
        for info in infos:
            author_url = base_url + info.xpath('a[1]/@href').extract()[0]
            name = info.xpath('a[1]/h4/text()').extract()[0].strip()
            recent_article = info.xpath('div[@class="recent-update"]')[0].xpath('string(.)').extract()[0].strip().replace('\n', '')
            yield Request(author_url, meta={'author_url': author_url, 'name': name, 'recent_article': recent_article}, callback=self.parse_item)
        urls = ['https://www.jianshu.com/recommendations/users?page={}'.format(str(i)) for i in range(2, 100)]
        for url in urls:
            yield Request(url, callback=self.parse)

    def parse_item(self, response):
        item = JianshuAuthorItem()
        item['author_url'] = response.meta['author_url']
        item['name'] = response.meta['name']
        item['recent_article'] = response.meta['recent_article']

        selector = Selector(response)
        type1 = selector.xpath('//ul[@class="list user-dynamic"]')
        type0 = selector.xpath('//ul[@class="list user-dynamic"]').xpath('string(.)').extract()[0].strip().replace('\n', '')
        detail = selector.xpath('//div[@class="main-top"]/div[@class="info"]/ul')
        focus = detail.xpath('li[1]/div[1]/a[1]/p/text()').extract()[0]
        fans = detail.xpath('li[2]/div[1]/a[1]/p/text()').extract()[0]
        article_number = detail.xpath('li[3]/div[1]/a[1]/p/text()').extract()[0]
        words = detail.xpath('li[4]/div[1]/p/text()').extract()[0]
        like = detail.xpath('li[5]/div[1]/p/text()').extract()[0]

        item['type'] = type0
        item['focus'] = focus
        item['fans'] = fans
        item['article_number'] = article_number
        item['words'] = words
        item['like'] = like
        yield item
