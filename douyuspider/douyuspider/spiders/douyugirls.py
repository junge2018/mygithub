# -*- coding: utf-8 -*-
import scrapy
from douyuspider.items import DouyuItem
import json

class DouyugirlsSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['capi.douyucdn.cn']
    url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='
    offset = 0
    start_urls = [url+str(offset)]

    def parse(self, response):
        data_list = json.loads(response.text)['data']
        for tem in data_list:
            items = DouyuItem()
            items['nickname'] = tem['nickname']
            items['imagelink'] = tem['vertical_src']

            yield items

        if self.offset < 220:
            self.offset += 20
        else:
            break

        yield scrapy.Request(self.url+str(self.offset), callback=self.parse)
