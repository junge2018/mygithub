# -*- coding:utf-8 -*-

import urllib, urllib2
from lxml import etree


class Tie_ba:
    def __init__(self):
        self.filename = ''
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1;) AppleWebKit/537 (KHTML, like Gecko) Chrome/70 Safari/537.36'}
        self.page = 1

    def load_page(self, url):
        """
        作用：根据url发送请求，获取服务器响应文件
        url：需要爬取的url地址
        filename: 文件名
        """
        print ('正在下载: ' + self.filename)
        request = urllib2.Request(url, headers=self.header)
        html = urllib2.urlopen(request).read()
        content = etree.HTML(html)
        link_list = content.xpath('//div[@class="threadlist_lz clearfix"]//a[@class="j_th_tit"]/@href')
        i = 1
        for link in link_list:
            link = 'https://tieba.baidu.com' + link
            self.load_image(link, i)
            i += 1

    def load_image(self, link, n):
        print ('正在下载: ' + self.filename + '-第'+str(n)+'条帖子')
        request = urllib2.Request(link, headers=self.header)
        html = urllib2.urlopen(request).read()
        content = etree.HTML(html)
        link_list = content.xpath('//cc//img[@class="BDE_Image"]/@src')
        i = 1
        for link_tem in link_list:
            self.write_image(link_tem, i)
            i += 1
        print ('下载完毕: ' + self.filename + '-第' + str(n) + '条帖子')

    def write_image(self, link, i):
        """
        作用：保存服务器响应文件到本地磁盘文件里
        html: 服务器响应文件
        filename: 本地磁盘文件名
        """
        # with open方法相当于执行了open - write - close三步操作，后面不用再close文件了
        print ('正在存储: ' + self.filename + '-图片' + str(i))
        pic_name = str(i) + '.jpg'
        request = urllib2.Request(link, headers=self.header)
        image_tem = urllib2.urlopen(request).read()
        with open('./pic'+str(self.page)+'/'+pic_name.decode('utf-8'), 'wb') as f:
            f.write(image_tem)

    def tieba_spider(self, url, begin_page, end_page, kw):
        """
        作用：负责处理url，分配每个url去发送请求
        url：需要处理的第一个url
        begin_page: 爬虫执行的起始页面
        end_page: 爬虫执行的截止页面
        """
        for page in range(begin_page, end_page + 1):
            page_num = (page - 1)*50
            self.page = page
            urlfull = url + '&pn=' + str(page_num)
            self.filename = '贴吧-' + kw + '-第' + str(page) + '页'
            self.load_page(urlfull)

if __name__ == '__main__':
    """主控制程序"""
    kw = raw_input('请输入需要爬取的贴吧名:')
    begin_page = int(raw_input('请输入起始页码:'))
    end_page = int(raw_input('请输入结尾页码:'))

    url = 'http://tieba.baidu.com/f?'
    title = urllib.urlencode({'kw': kw})
    urlfull = url + title

    tie = Tie_ba()
    tie.tieba_spider(urlfull, begin_page, end_page, kw)
