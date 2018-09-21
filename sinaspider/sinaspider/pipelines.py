# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SinaPipeline(object):
    def open_spider(self, spider):
        print u'开始爬取'.encode('gbk')

    def process_item(self, item, spider):
        final_url = item['final_url']
        content = item['title']+'\r\n'+final_url+'\r\n'+'-'*120+'\r\n'+item['content']+'\r\n'+'='*120+'\r\n'

        filename = final_url[7:-6].replace('/', '_')+'.txt'
        file_dir = item['sub_filename']
        with open(file_dir+'\\'+filename, 'w') as f:
            f.write(content)

        return item

    def close_spider(self, spider):
        print u'爬取结束'.encode('gbk')
