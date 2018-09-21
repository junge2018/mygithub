# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dongguanspider.items import DongguanItem

class DongguanSpider(CrawlSpider):
    name = 'dongguan'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=0']

    rules = (
        Rule(LinkExtractor(allow=(r'type=4&page=\d+'))),
        Rule(LinkExtractor(allow=r'question/\d+/\d+.shtml'), callback='parse_item'),
    )
    """
    def deal_links(self,links):
        print links
        for link in links:
            link.url = link.url.replace('http', 'HTTP')
        print links
        return links
    """

    def parse_item(self, response):
        # print response.url
        # '''
        item = DongguanItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        item['title'] = response.xpath('//div[@class="pagecenter p3"]//strong[@class="tgray14"]/text()').extract()[0]
        item['serial'] = item['title'].split(' ')[-1].split(':')[-1]
        con = response.xpath('//div[@class="c1 text14_2"]/div[@class="textpic"]')
        if len(con) == 0:
            tem = response.xpath('//div[@class="c1 text14_2"]/text()').extract()
            item['content'] = ''.join(tem).strip().replace(u'\xa0', ' ')
            item['im_link'] = 'No'
        else:
            tem = con.xpath('../div[@class="contentext"]/text()').extract()
            item['content'] = ''.join(tem).strip().replace(u'\xa0', ' ')
            link_tem = con.xpath('./img/@src').extract()[0]
            item['im_link'] = 'http://wz.sun0769.com'+link_tem
            yield scrapy.Request(item['im_link'],callback=self.parse_image)
        item['link'] = response.url

        yield item
        # '''

    def parse_image(self, response):
        url = response.url
        name = url[-11:]
        with open('.\\images\\'+name, 'wb') as f:
            f.write(response.body)
