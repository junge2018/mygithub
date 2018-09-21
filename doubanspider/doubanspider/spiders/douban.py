# -*- coding: utf-8 -*-
import scrapy
from doubanspider.items import DoubanItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    url = 'https://movie.douban.com/top250?start='
    offset = 0
    start_urls = [url+str(offset)]

    def parse(self, response):
        node_list = response.xpath('//div[@class="info"]')
        for node in node_list:
            item = DoubanItem()
            item['title']= node.xpath('.//a/span[1]/text()').extract()[0]
            actors = node.xpath('.//div[@class="bd"]/p[1]/text()').extract()
            item['bd']= ''.join(actors).strip()
            item['rating_num']= node.xpath('.//div[@class="star"]/span[2]/text()').extract()[0]
            item['quote']= node.xpath('.//div[@class="bd"]/p/span[@class="inq"]/text()').extract()[0]

            yield item

        if self.offset < 225:
            self.offset += 25
            yield scrapy.Request(self.url+str(self.offset), callback=self.parse)
