# -*- coding:utf-8 -*-
import urllib, urllib2


url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3528.4 Safari/537.36',
          'X-Requested-With': 'XMLHttpRequest',
          'Content-Type': 'application / x-www-form-urlencoded; charset = UTF-8',
          'Origin': 'http://fanyi.youdao.com',
          'Accept': 'application/json, text/javascript, */*; q=0.01'}
in_tem = raw_input('请输入查询英文:')
data_tem = {
    "i":in_tem,
    "smartresult":"dict",
    "client":"fanyideskweb",
    "doctype":"json",
    "version":"2.1",
    # "keyfrom":"fanyi-new.logo",
    "keyfrom":"fanyi.web",
    "action":"FY_BY_ENTER",
    "typoResult":"true",
    'ue':'UTF-8'
}
data1 = urllib.urlencode(data_tem)
request = urllib2.Request(url, data=data1, headers=header)
print urllib2.urlopen(request).read()
