# -*- coding:utf-8 -*-
import re, urllib2


class Nei_han:
    def __init__(self):
        self.page = 1
        self.switch = True

    def load_page(self):
        print '正在下载第' + str(self.page) + '页数据...'
        url = 'https://www.neihan8.com/article/list_5_' + str(self.page) + '.html'
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/54 Safari/537.36'}
        request = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(request)
        html = response.read()  # 拿到整个页面内容
        html_tem = html.decode('gbk').encode('utf-8')
        pattern = re.compile('<div\sclass="f18 mb20">(.*?)</div>', re.S)
        list_tem = pattern.findall(html_tem)
        # print html.decode('gbk')
        self.deal_page(list_tem)

    def deal_page(self, list_tem):
        print '正在写入第' + str(self.page) + '页数据...'
        i = 1
        with open('内涵段子.txt'.decode('utf-8'), 'a') as f:
            f.write('\n===内涵段子第' + str(self.page) + '页===')
            f.write('=' * 50)
        for content in list_tem:
            content = content.replace('<p>', '').replace('</p>', '').replace('<br>', '').replace('<br />', '').replace('&ldquo;', '\"').replace('&rdquo;', '\"').replace('&hellip;', '...')
            print ('--正在写入第%d页数据%d...' % (self.page, i))
            self.write_page(content)
            i += 1
        print '写入第' + str(self.page) + '页数据完毕'
        print ('='*30)

    def write_page(self, content):
        with open('内涵段子.txt'.decode('utf-8'), 'a') as f:
            f.write(content)
            f.write('*' * 30)
        print '--写入分条数据完毕'

    def handle_page(self):
        while self.switch:
            in_word = raw_input('按下回车开始爬取下一页数据(退出q或者quit)')
            if in_word == 'q' or in_word == 'quit':
                self.switch = False
                print "谢谢使用爬虫 版本:junge 1.10"
            else:
                self.load_page()
                self.page += 1

if __name__ == '__main__':
    """
        ======================
            内涵段子小爬虫
        ======================
    """
    ob = Nei_han()
    ob.handle_page()
