# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# from scrapy.pipelines.images import ImagesPipeline
import scrapy, json
from datetime import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class HongniangPipeline(object):
    # def __init__(self):
        # self.f = open('hongniang.json', 'w')

    def process_item(self, item, spider):
        item['crawl_time'] = datetime.now()
        item['spider'] = spider.name
        # content = json.dumps(dict(item), ensure_ascii=False)+'\n'
        # self.f.write(content)

        return item

    def open_spider(self, spider):
        print u'爬取开始'

    def close_spider(self, spider):
        # self.f.close()
        print u'爬取结束'

"""
# 分布式爬取，不爬取图片，只爬取内容写入Redis数据库
class ImagePipe(ImagesPipeline):
    # IMAGES_STORE = get_project_settings().get('IMAGE_STORE')

    def get_media_requests(self, item, info):
        items = item['image_urls'].split('|')[:-1]
        for url in items:
            yield scrapy.Request(url, meta={'it':item})

    def item_completed(self, results, item, info):
        if isinstance(item, dict) or self.images_result_field in item.fields:
            item[self.images_result_field] = [x for ok, x in results if ok]
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['it']
        image_guid = item['username'].split()[0]
        filename = '.\%s.jpg' % image_guid
        return filename
"""

