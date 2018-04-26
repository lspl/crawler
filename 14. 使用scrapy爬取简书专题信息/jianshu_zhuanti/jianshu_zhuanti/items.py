# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item


class JianshuZhuantiItem(Item):
    name = Field()
    introduction = Field()
    article_number = Field()
    fans = Field()
    pass
