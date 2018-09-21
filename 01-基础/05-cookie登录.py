# -*- coding:utf-8 -*-


import urllib2, cookielib, urllib


cookie_tem = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie_tem)

filename = 'cookie.txt'
cookie_tem1 = cookielib.MozillaCookieJar(filename)
handler1 = urllib2.HTTPCookieProcessor(cookie_tem1)

opener = urllib2.build_opener(handler, handler1)
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0;) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/54 Safari/537.36')]
da = {'email': '734930080@qq.com', 'password': 'liu18972997791'}
data1 = urllib.urlencode(da)
request = urllib2.Request('http://www.renren.com/PLogin.do', data=data1)
# print opener.open(request).read()
opener.open(request)
cookie_tem1.save()
print opener.open('http://www.renren.com/362337072/profile').read()