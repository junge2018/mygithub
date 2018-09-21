# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.project import get_project_settings
from scrapy.pipelines.images import ImagesPipeline
import scrapy, os
import codecs

class DongguanspiderPipeline(object):
    def __init__(self):
        self.file = codecs.open('tencent.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        title = item['title']
        serial = item['serial']
        content = item['content']
        link = item['link']
        text = title+'\t'+serial+'\r\n'+link+'\r\n'+content+'\r\n'
        self.file.write(text+'*'*130+'\r\n')
        return item

    def open_spider(self, spider):
        print u'开始爬取'.encode('gbk')

    def close_spider(self, spider):
        self.file.close()
        print u'爬取完毕'.encode('gbk')

'''
class ImagePipeline(ImagesPipeline):
    image_store = get_project_settings().get('IMAGE_STORE')

    def get_media_requests(self, item, info):
        image_url = item['im_link']
        yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]

        os.rename(self.image_store+'\\'+image_path[0], self.image_store+'\\'+item['title']+'.jpg')
        return item
'''
