# -*- coding:utf-8 -*-

import urllib, urllib2


def load_page(url, filename):
    """
    作用：根据url发送请求，获取服务器响应文件
    url：需要爬取的url地址
    filename: 文件名
    """
    print ('正在下载: ' + filename)
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1;) AppleWebKit/537 (KHTML, like Gecko) Chrome/70 Safari/537.36'}
    request = urllib2.Request(url, headers=header)
    return urllib2.urlopen(request).read()


def write_page(html, filename):
    """
    作用：保存服务器响应文件到本地磁盘文件里
    html: 服务器响应文件
    filename: 本地磁盘文件名
    """
    # with open方法相当于执行了open - write - close三步操作，后面不用再close文件了
    print ('正在存储: ' + filename)
    with open(filename.decode('utf-8'), 'w') as f:
        f.write(html)
    print '-'*30


def tieba_spider(url, begin_page, end_page, kw):
    """
    作用：负责处理url，分配每个url去发送请求
    url：需要处理的第一个url
    begin_page: 爬虫执行的起始页面
    end_page: 爬虫执行的截止页面
    """
    for page in range(begin_page, end_page + 1):
        page_num = (page - 1)*50
        urlfull = url + '&pn=' + str(page_num)
        filename = '贴吧-' + kw + '-第' + str(page) + '页.html'
        html = load_page(urlfull, filename)
        write_page(html, filename)

if __name__ == '__main__':
    """主控制程序"""
    kw = raw_input('请输入需要爬取的贴吧名:')
    begin_page = int(raw_input('请输入起始页码:'))
    end_page = int(raw_input('请输入结尾页码:'))

    url = 'http://tieba.baidu.com/f?'
    title = urllib.urlencode({'kw': kw})
    urlfull = url + title

    tieba_spider(urlfull, begin_page, end_page, kw)
