# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HongniangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    username = scrapy.Field()
    age = scrapy.Field()
    workplace = scrapy.Field()
    house = scrapy.Field()
    content = scrapy.Field()
    image_urls = scrapy.Field()
    profile = scrapy.Field()
    crawl_time = scrapy.Field()
    spider = scrapy.Field()

