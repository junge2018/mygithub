# -*- coding: utf-8 -*-
import scrapy
from sinaspider.items import SinaspiderItem
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        parent_titles = response.xpath('//div[@id="tab01"]/div/h3/a/text()').extract()
        parent_urls = response.xpath('//div[@id="tab01"]/div/h3/a/@href').extract()

        #第一级总的--地方站--无a标签连接,只有标题
        parent_otitle = response.xpath('//div[@id="tab01"]/div/h3/span/text()').extract()
        parent_titles += parent_otitle
        parent_urls += [u'http://city.sina.com.cn/']

        sub_titles = response.xpath('//div[@id="tab01"]/div/ul[@class="list01"]/li/a/text()').extract()
        sub_urls = response.xpath('//div[@id="tab01"]/div/ul[@class="list01"]/li/a/@href').extract()

        # 爬取所有大类
        for i in range(0, len(parent_titles)):
            parent_filename = '.\\data\\'+parent_titles[i]
            if not os.path.exists(parent_filename):
                os.makedirs(parent_filename)

            items = []
            for j in range(0, len(sub_urls)):
                item = SinaspiderItem()
                item['parent_title'] = parent_titles[i]
                item['parent_url'] = parent_urls[i]
                # 结尾为.sina.com.cn/都存放在地方站
                if i == len(parent_titles)-1:
                    if_belong = sub_urls[j].endswith('.sina.com.cn/')
                else:
                    # 检查小类链接开头是否属于大类，属于就存放在大类下
                    if_belong = sub_urls[j].startswith(item['parent_url'])  # 返回true or false

                if if_belong:
                    sub_filename = parent_filename+'\\'+sub_titles[j]
                    if not os.path.exists(sub_filename):
                        os.makedirs(sub_filename)

                    item['sub_title'] = sub_titles[j]
                    item['sub_url'] = sub_urls[j]
                    item['sub_filename'] = sub_filename
                    items.append(item)

            for item in items:
                yield scrapy.Request(item['sub_url'], meta={'meta_1': item}, callback=self.parse_second)

    # 处理小类提取到的链接
    def parse_second(self, response):
        # 提取传过来的meta字典类的键的值
        meta_1 = response.meta['meta_1']  # 值为item字典对象
        final_url = response.xpath('//a/@href').extract()

        items = []
        for i in range(0, len(final_url)):
            if meta_1['parent_url'] == u'http://city.sina.com.cn/':
                if_belong = final_url[i].startswith(meta_1['sub_url']) and final_url[i].endswith('.shtml')
            else:
                if_belong = final_url[i].startswith(meta_1['parent_url']) and final_url[i].endswith('.shtml')

            # 如果属于一个大类，那么就用一个item整合信息便于传输
            if if_belong:
                item = SinaspiderItem()
                item['parent_title'] = meta_1['parent_title']
                item['parent_url'] = meta_1['parent_url']
                item['sub_title'] = meta_1['sub_title']
                item['sub_url'] = meta_1['sub_url']
                item['sub_filename'] = meta_1['sub_filename']
                item['final_url'] = final_url[i]
                items.append(item)

        for item in items:
            yield scrapy.Request(item['final_url'], meta={'meta_2': item}, callback=self.parse_detail)

    # 处理子类里面的每个详情页的请求，获取文章和标题
    def parse_detail(self, response):
        meta_2 = response.meta['meta_2']
        tit_xp = ('//h1[@class="main-title"]/text() | //div[@id="artibody"]/div/h1/text()'
                  ' | //h1[@id="artibodyTitle"]/text() | //span[@class="location"]/h1/text()'
                  ' | //h1[@id="j_title"]/text() | //body[@class="skin-ent"]/div/a/text()'
                  ' | //h1[@id="main_title"]/text() | //h2[@id="artibodyTitle"]/text()')
        title = response.xpath(tit_xp).extract()

        con_xp = ('//div[@class="article"]//p/text() | //div[@class="article-body main-body"]/p/text()'
                  ' | //div[@id="artibody"]/p//text() | //body[@class="skin-ent"]/div/a/@href'
                  ' | //div[@class="article-content-left"]/div[@class="article"]/div/text()')
        content_tem = response.xpath(con_xp).extract()

        if len(title) == 0:
            meta_2['title'] = u'未找到标题'
        elif len(title) == 1:
            meta_2['title'] = title[0]
        else:
            tit = u''
            for t in title:
                tit += t + '\r\n'+'*'*60+'\r\n'
            meta_2['title'] = tit

        # 内容的p标签很多个，需要组合在一起
        content = u''
        if len(content_tem) == 0 and len(title) == 0:
            return
        elif len(content_tem) == 0:
            content = u'内容为空'
        else:
            for con in content_tem:
                content += con.strip() + '\r\n'

        meta_2['content'] = content

        yield meta_2

