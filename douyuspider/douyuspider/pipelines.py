# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class DouyuspiderPipeline(object):
#     def process_item(self, item, spider):
#         return item
import scrapy
# 导入此类，可以从settings.py文件中取值,取出图片路径
from scrapy.utils.project import get_project_settings
from scrapy.pipelines.images import ImagesPipeline
import os


# 此法继承父级为图片管道处理类
class ImagePipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        image_url = item['imagelink']
        yield scrapy.Request(image_url)
        # 此法只发送请求，completed处理图片

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]

        os.rename(self.IMAGES_STORE+'\\'+image_path[0], self.IMAGES_STORE+'\\'+item['nickname']+'.jpg')
        item['imagepath'] = self.IMAGES_STORE+'\\'+item['nickname']+'.jpg'
        return item
