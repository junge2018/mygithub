# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import unittest, time


class spider_detail(unittest.TestCase):
    def setUp(self):
        options = Options()
        # options.set_headless()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options = options)
        self.douyu_usernum = 0
        self.page = 1

    def testHtml(self):
        print '开始爬取数据...'
        self.driver.get('http://www.douyu.com/directory/all')
        time.sleep(1)
        while True:
            html = self.driver.page_source
            last_page = html.find('shark-pager-disable-next')
            soup = BeautifulSoup(html, 'lxml')
            douyu_titles = soup.find_all('h3',{'class': 'ellipsis'})
            douyu_types = soup.find_all('span', {'class': 'tag ellipsis'})
            douyu_usernames = soup.find_all('span', {'class': 'dy-name ellipsis fl'})
            douyu_nums = soup.find_all('span', {'class': 'dy-num fr'})

            douyu_list = zip(douyu_titles, douyu_types, douyu_usernames, douyu_nums)
            s_str = ''
            for douyu_title,douyu_type,douyu_username,douyu_num in douyu_list:
                title = douyu_title.get_text().strip()
                dtype = douyu_type.get_text().strip()
                name = douyu_username.get_text().strip()
                num = douyu_num.get_text().strip()
                s_tem = (u'斗鱼房间标题:'+title.ljust(42-len(title.encode('gb18030','ignore'))+len(title))+'\t'+
                         u'斗鱼房间类型:'+dtype.ljust(26-len(dtype.encode('gb18030','ignore'))+len(dtype))+'\t'+
                         u'斗鱼房间用户名:'+name.ljust(22-len(name.encode('gb18030','ignore'))+len(name))+'\t'+
                         u'斗鱼房间热度值:'+num.ljust(10-len(num.encode('gb18030','ignore'))+len(num))+'\n')
                s_str += s_tem
                self.douyu_usernum += 1

            with open('22斗鱼房间信息.txt'.decode('utf-8').encode('utf-8'), 'a') as f:
                f.write(s_str.encode('utf-8'))

            if last_page != -1:
                break
            self.driver.find_element_by_class_name('shark-pager-next').click()
            self.page += 1

    def tearDown(self):
        print '爬取完成，关闭浏览器，共有%d页' % self.page
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
