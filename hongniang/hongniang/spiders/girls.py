# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from hongniang.items import HongniangItem
from scrapy_redis.spiders import RedisCrawlSpider

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class GirlsSpider(RedisCrawlSpider):
    name = 'girls'
    # allowed_domains = ['hongniang.com']
    # start_urls = (['http://www.hongniang.com/index/search?sort=0&wh=0&sex=2&starage=2&province=湖北&city=武汉&marriage=1'
    #                '&edu=0&income=0&height=0&pro=0&house=0&child=0&xz=0&sx=0&mz=0&hometownprovince=0&zhiye=&page=1'])

    redis_key = 'girlsspider:start_urls'
    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None,domain.split(','))
        super(GirlsSpider,self).__init__(*args, **kwargs)

    # 拿到所有页面
    page_list = LinkExtractor(allow=(r'sort=0&wh=0&sex=2&starage=2&province.*page=\d+'),)
    # 拿到页面内所有用户链接
    user_list = LinkExtractor(allow=r'/user/member/id/\d+',)

    rules = (
        Rule(page_list, follow=True),
        Rule(user_list, callback='parse_item')
    )
    '''
    def deal_links(self, links):
        for link in links:
            link.url = 'http://www.hongniang.com/index/search' + link.url
        print links
        return links
    '''

    """
    # 登录网站
    def start_requests(self):
        url = 'http://www.hongniang.com/account/login'
        yield scrapy.Request(url, callback=self.post_login, meta={'cookiejar':1}, dont_filter=True)

    def post_login(self, response):
        print u'正在登录'.encode('gbk')
        verify = 'http://www.hongniang.com' + response.xpath('//img[@class="verify_img"]/@src').extract()[0]
        image_file = r'D:\python_temp\spider\hongniang\verify.png'
        urllib.urlretrieve(verify, image_file)
        print u'验证码写入完毕'.encode('gbk')
        print response.meta['cookiejar']
        verify_in = raw_input(u'请输入验证码:'.encode('gbk'))
        yield scrapy.FormRequest.from_response(
            response,
            meta={'cookiejar':response.meta['cookiejar']},
            formdata={'username': '18972997791', 'password': 'qq970430670', 'verify': str(verify_in)},
            callback=self.login_after,
            dont_filter=True
        )

    def login_after(self, response):
        logout = response.xpath('//a[@id="logout"]/text()').extract()
        if len(logout):
            print u'登录成功'.encode('gbk')
            for url in self.start_urls:
                yield self.make_requests_from_url(url)
        else:
            print u'登录失败'.encode('gbk')
    """

    cookies = {
        'CwCzwf_userid': '11003847',
        'Hm_lvt_13345a0835e13dfae20053e4d44560b9': '1536581193,1536590175,1536621695,1536745948',
        'Hm_lpvt_13345a0835e13dfae20053e4d44560b9': '1536754440',
        'PHPSESSID': 'uhkn81s9u56n2hm3i2vq3qb5o1'

    }

    def start_requests(self):
        url = 'http://www.hongniang.com/index.php'
        yield scrapy.FormRequest(url, cookies=self.cookies, callback=self.login_after, dont_filter=True)

    def login_after(self, response):
        logout = response.xpath('//a[@id="logout"]/text()').extract()
        if len(logout):
            print (u'登录成功:'+logout[0])
            # yield self.make_requests_from_url(self.start_urls[0])
        else:
            print u'登录失败'

    def parse_item(self, response):
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        item = HongniangItem()
        item['username'] = self.get_username(response)
        item['age'] = self.get_age(response)
        item['workplace'] = self.get_workplace(response)
        item['house'] = self.get_house(response)
        item['content'] = self.get_content(response)
        item['image_urls'] = self.get_image_urls(response)
        item['profile'] = response.url

        yield item

    def get_username(self, response):
        usernames = response.xpath('//div[@class="name nickname"]/text()[1]').extract()
        userids = response.xpath('//div[@class="loveid"]/text()').extract()
        if len(userids):
            username = usernames[0].strip() + '  ' + userids[0]
        else:
            username = u'未找到用户名和id'
        return username

    def get_age(self, response):
        ages = response.xpath('//div[@class="info2"]/div/ul[1]/li//text()').extract()
        if len(ages) == 4:
            age = ages[0].strip()+ages[1].strip()+'  '+ages[2].strip()+ages[3].strip()
        else:
            age = u'年龄:null,婚况:null...'
        return age

    def get_workplace(self, response):
        workplaces = response.xpath('//div[@class="info2"]/div/ul[3]/li[2]//text()').extract()
        if len(workplaces) == 2:
            workplace = workplaces[0].strip()+workplaces[1].strip()
        else:
            workplace = u'工作地:null'
        return workplace

    def get_house(self, response):
        house_tem = response.xpath('//div[@class="sub2"]/div[1]/div[@class="right"]/ul[2]/li//text()').extract()
        if len(house_tem) > 5:
            house = ''
            for h in house_tem:
                house += h.strip() + '  '
        else:
            house = u'籍贯和住房条件不可知...'
        return house

    def get_content(self, response):
        contents = response.xpath('//div[@class="info5"]/div/text()').extract()
        if len(contents) == 2:
            content = contents[0].strip()+contents[1].strip()
        else:
            content = u'内心独白:null'
        return content

    def get_image_urls(self, response):
        image_urls = response.xpath('//ul[@id="tFocus-pic"]/li//img/@src').extract()
        if len(image_urls):
            image_url = ''
            for i in image_urls:
                if i.startswith('http://www.hongniang.com'):
                    image_url += i + '|'
                else:
                    image_url += 'http://www.hongniang.com' + i + '|'
        else:
            image_url = u'null'
        return image_url


