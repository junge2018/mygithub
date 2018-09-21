# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo

class DoubanspiderPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        sheetname = settings['MONGODB_SHEETNAME']

        client = pymongo.MongoClient(host=host, port=port)
        mdb = client[dbname]
        self.msheet = mdb[sheetname]

    def process_item(self, item, spider):
        data = dict(item)
        self.msheet.insert(data)
        return item
