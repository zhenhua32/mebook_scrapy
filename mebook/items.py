# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MebookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    baidu = scrapy.Field()
    baidu_key = scrapy.Field()
    tianyi = scrapy.Field()
    tianyi_key = scrapy.Field()
    chengtong = scrapy.Field()
