# coding=utf-8

from lxml import etree
import requests, os, json

class Qiushi:
	def __init__(self):
		self.page = 1
		self.header = {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'}

	def spider(self):
		start_page = raw_input('请输入起始页(>=1):')
		end_page = raw_input('请输入结束页(>=1):')
		for page in range(int(start_page), int(end_page)+1):
			self.page = page
			os.mkdir('00'+str(page)+'糗事百科第'+str(page)+'页')
			self.load_page(page)
			print '第'+str(page)+'页数据写入完毕'

	def load_page(self, page):
		url = 'https://www.qiushibaike.com/8hr/page/'+str(page)+'/'
		html = requests.get(url,headers=self.header).text
		content = etree.HTML(html)
		node_list = content.xpath('//div[contains(@id,"qiushi_tag")]')
		con_list = []
		i = 1
		for node in node_list:
			con_dict = {}
			username = node.xpath('./div//h2')[0].text
			if username == '匿名用户'.decode('utf-8'):
				age = '32null'
			else:
				age = node.xpath('./div/div')[0].text
			article_li = node.xpath('./a[@class="contentHerf"]/@href')[0]
			article_link = 'https://www.qiushibaike.com' + article_li
			image_tem = node.xpath('./div/a/img[@class="illustration"]/@src')
			if image_tem==[]:
				image=''
			else:
				image = 'https:'+image_tem[0]
			zan = node.xpath('.//span/i')[0].text
			comments = node.xpath('.//span/a/i')[0].text

			article = self.load_detail(article_link, image, i)
			con_dict = {
				"username" : username.replace('\n', ''),
				"age" : age,
				"zan" : zan,
				"comments" : comments,
				'article' : article,
				'image' : image,
			}
			i += 1
			con_list.append(con_dict)

		self.write_page(con_list)

	def load_detail(self, a_link, i_link, i):
		html = requests.get(a_link,headers=self.header).text
		content = etree.HTML(html)
		article_tem = content.xpath('//div[@id="single-next-link"]/div[@class="content"]')[0].text.replace('\n', '')

		if i_link != '':
			image = requests.get(i_link,headers=self.header).content
			self.write_image(image, i)

		return article_tem

	def write_image(self,image, i):
		print '正在写入图片'+str(i)+'...'
		with open('00'+str(self.page)+'糗事百科第'+str(self.page)+'页'+'/'+'qiushi'+str(i)+'.jpg'.decode('utf-8').encode('utf-8'), 'wb') as f:
			f.write(image)

	def write_page(self, li):
		print '正在写入json数据...'
		f = open('00'+str(self.page)+'糗事百科第'+str(self.page)+'页'+'/'+'qiushi.json'.decode('utf-8').encode('utf-8'), 'w')
		for item in li:
			f.write(json.dumps(item, ensure_ascii=False).encode('utf-8')+'\n')
		f.close()
		print '写入json数据完毕'


if __name__ == '__main__':
	qiushi = Qiushi()
	qiushi.spider()


