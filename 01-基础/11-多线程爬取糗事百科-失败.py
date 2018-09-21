# -*- coding:utf-8 -*-

import threading
from Queue import Queue
import requests, os
from lxml import etree
import json, random
import traceback

user_agent_list = [
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
	"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
	"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
	"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
	"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
	"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
	"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
]

# 继承父类，重写或者加写其中内容
class Thread_crawl(threading.Thread):
	def __init__(self, tname, page_queue):
		super(Thread_crawl, self).__init__()  # super法较为完善的继承父类init方法
		self.tname = tname
		self.page_queue = page_queue
		global user_agent_list
		h_tem = random.choice(user_agent_list)
		self.header = {'User-Agent': h_tem}

	# 此run方法被彻底改写，线程的start()首先调用此改写的run而不去调用父类的原始方法,start自动执行
	def run(self):
		print 'start_thread:'+self.tname  # 字符串加可以
		self.spider()
		print 'end_thread:', self.tname  # 多个一起打印输出，中间用逗号

	def spider(self):
		# get方法从队列中最前取出一个值并删除队列中的值
		# get方法有一个可选参数block阻塞,默认为True
		# get(True)则当队列为空，调用的线程阻塞，等待队列有值马上继续任务，没有值一直等待，适合动态加入数据的线程
		# get(False)则当队列为空，调用的线程直接返回Queue.empty()的异常，但不停止线程，适合队列值固定，不需要队列为空时等待任务
		global data_queue
		global crawl_exit  # 声明全局变量，预防线程内部无法读取全局变量
		while not crawl_exit:
			try:
				page = self.page_queue.get(False)
				# 页码队列固定，为空则所有页码处理完，线程通过异常走except再次循环，否则阻塞卡在get这里无法向下执行
				url = 'https://www.qiushibaike.com/8hr/page/' + str(page) + '/'
				html = requests.get(url, headers=self.header).text
				data_queue.put(html)
			except Exception, e:
				pass


# 继承父类，重写或者加写其中内容
class Thread_parse(threading.Thread):
	def __init__(self, parsename, lock1, lock2):
		super(Thread_parse, self).__init__()  # super法较为完善的继承父类init方法
		self.parsename = parsename
		global user_agent_list
		h_tem = random.choice(user_agent_list)
		self.header = {'User-Agent': h_tem}
		self.lock1 = lock1  # 线程锁，一次只有一个线程可以使用
		self.lock2 = lock2

	def run(self):
		print 'start_parse:'+self.parsename  # 字符串加可以
		global data_queue
		global parse_exit
		while not parse_exit:
			try:
				html = data_queue.get(False)
				self.parse(html)
				data_queue.task_done()
			except Exception, e:
				e1 = traceback.format_exc()
				print '解析错误:', e1
		print 'end_parse:', self.parsename

	def parse(self, html):
		content = etree.HTML(html)
		node_list = content.xpath('//div[contains(@id,"qiushi_tag")]')
		con_list = []
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
			with self.lock1:
				article = self.load_detail(article_link, image)
			con_dict = {
				"username" : username.replace('\n', ''),
				"age" : age,
				"zan" : zan,
				"comments" : comments,
				'article' : article,
				'image' : image,
			}
			con_list.append(con_dict)
		with self.lock1:
			self.write_page(con_list)

	def load_detail(self, a_link, i_link):
		html = requests.get(a_link, headers=self.header).text
		content = etree.HTML(html)
		article_tem = content.xpath('//div[@id="single-next-link"]/div[@class="content"]')[0].text.replace('\n', '')

		if i_link != '':
			image = requests.get(i_link, headers=self.header).content
			self.write_image(image)

		return article_tem

	def write_image(self, image):
		global num
		# 此方法自动上锁，执行完后自动释放锁，即lock.acquire+处理完毕+lock.release
		with open('111糗事百科'+'/'+'qs' + str(num) + '.jpg'.decode(
				'utf-8').encode('utf-8'), 'wb') as f:
			f.write(image)
		num += 1

	def write_page(self, li):
		global total
		f = open('111糗事百科'+'/'+'qiushi.json'.decode('utf-8').encode('utf-8'), 'a')
		comment = {'页码'.decode('utf-8'): '='*20+'第'.decode('utf-8')+str(int(total/25)+1)+'页'.decode('utf-8')+'='*20}
		f.write(json.dumps(comment, ensure_ascii=False).encode('utf-8') + '\n')
		for item in li:
			f.write(json.dumps(item, ensure_ascii=False).encode('utf-8') + '\n')
			total += 1
		f.close()


# 全局变量的一个控制线程循环的开关
data_queue = Queue()
crawl_exit = False
parse_exit = False
num = 1  # 图片命名
total = 0  # 写入数据总条数
lock1 = threading.Lock()
lock2 = threading.Lock()

def main():
	# 存放爬取页码范围
	page_queue = Queue(100)
	start_page = raw_input('请输入起始页(>=1):')
	end_page = raw_input('请输入结束页(<=100):')
	for page in range(int(start_page), int(end_page) + 1):
		page_queue.put(page)
	# 存放爬取的网页源码，一个个的存进去，先进先出
	os.mkdir('111糗事百科')
	# 存放爬取的线程
	thread_list = []
	tname_list = ['采集线程1号', '采集线程2号', '采集线程3号']
	# 通过循环开启线程,此时data队列开始有数据，同时开启解析线程
	for tname in tname_list:
		thread = Thread_crawl(tname, page_queue)  # 此为重写threading.Thread线程类
		thread.start()
		thread_list.append(thread)

	# 通过循环开启解析线程
	global lock1
	global lock2
	parse_list = []
	parse_name = ['解析线程1', '解析线程2', '解析线程3']
	for parsename in parse_name:
		thread = Thread_parse(parsename, lock1, lock2)
		thread.start()
		parse_list.append(thread)

	# 当需要爬取的页面不为空的时候,主线程再次无限循环等待，为空时跳出循环，顺序往下执行
	while not page_queue.empty():
		pass
	global crawl_exit
	crawl_exit = True
	# 让抓取的线程停止循环，线程继续其任务直至结束
	# 主线程按照顺序往下执行，不会等待子进程，需要开启主进程等待
	for thread_tem in thread_list:
		thread_tem.join()

	print '所有页码抓取完毕，存放在数据队列'

	global data_queue

	# 解析线程解析的data_queue不为空时等待解析完毕
	global parse_exit
	while not data_queue.empty():
		pass
	parse_exit = True
	# 让解析的线程停止循环，线程继续其任务直至结束
	# 主线程按照顺序往下执行，不会等待子进程，需要开启主进程等待
	for parse_tem in parse_list:
		parse_tem.join()

	global total
	print '所有页码解析完毕，存放在本地-111糗事百科-文件夹==共有信息%d条' %total


if __name__ == '__main__':
	main()
