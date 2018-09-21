# -*- coding:utf-8 -*-
import urllib, urllib2


url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action='
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3528.4 Safari/537.36'}

data_tem = {
    'start': '0',
    'limit': '20'
}

data1 = urllib.urlencode(data_tem)
request = urllib2.Request(url, data=data1)
print urllib2.urlopen(request).read()
