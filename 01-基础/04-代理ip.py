# -*- coding:utf-8 -*-
import urllib2


url = 'http://www.baidu.com/'
proxy_in = False

proxy_tem = urllib2.ProxyHandler({'http': '112.115.57.20:3128'})
nullproxy_tem = urllib2.ProxyHandler({})

if proxy_in:
    opener = urllib2.build_opener(proxy_tem)
else:
    opener = urllib2.build_opener(nullproxy_tem)
request = urllib2.Request(url)
response = opener.open(request)
print response.read().decode('utf-8')


