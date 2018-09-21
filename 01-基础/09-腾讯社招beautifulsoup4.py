# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests

class Tencent:
    def __init__(self):
        self.header = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'}
        self.page = 1

    def spider(self):
        start_page = raw_input('请输入起始页(>=1):')
        end_page = raw_input('请输入结束页:')
        for page in range(int(start_page), int(end_page)+1):
            self.page = page
            page = (page - 1) * 10
            self.load_page(page)

    def load_page(self, page):
        url = 'https://hr.tencent.com/position.php?&'
        data = {'start': str(page)}
        response = requests.get(url, data, headers=self.header)
        page_name = '腾讯社招第'+str(self.page)+'页内容'
        print page_name

        with open('00腾讯社招详细内容.txt'.decode('utf-8'), 'a') as f:
            f.write(page_name)
            f.write('\n')
            f.write('='*100)
            f.write('\n')

        html = response.text.encode('utf-8')

        soup = BeautifulSoup(html, 'lxml')
        title = soup.select('.tablelist tr')
        i = 0
        list_tem = []  # [{},{},{}, ...]
        for tem in title[:-1]:
            content = {}
            content_list = tem.select('td')
            if i == 0:
                job_name = content_list[0].get_text()
                job_link = ''
                i += 1
            else:
                job_name = content_list[0].select('a')[0].get_text()
                job_li = content_list[0].select('a')[0].attrs['href']
                job_link = 'https://hr.tencent.com/'+job_li
            job_ty = content_list[1].get_text()
            job_num = content_list[2].get_text()
            work_location = content_list[3].get_text()
            pub_time = content_list[4].get_text()
            content['job_name'] = job_name
            content['job_link'] = job_link
            content['job_ty'] = job_ty
            content['job_num'] = job_num
            content['work_location'] = work_location
            content['pub_time'] = pub_time

            if job_link != '':
                job_detail = self.load_detail(job_link)
                content['job_detail'] = job_detail
            else:
                content['job_detail'] = ''

            list_tem.append(content)
        self.write_item(list_tem)

    def load_detail(self, link):
        response = requests.get(link, headers=self.header)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        title = soup.select('tr[class="c"] td div[class="lightblue"]')
        job_duty = title[0].get_text()
        job_require = title[1].get_text()

        ul_tem = soup.select('tr[class="c"] td ul[class="squareli"]')
        content1 = ''
        for item in ul_tem[0].select('li'):
            content1 += item.get_text()+'\n'
        job_duty += '\n'+content1

        content2 = ''
        for tem in ul_tem[1].select('li'):
            content2 += tem.get_text() + '\n'
        job_require += '\n' + content2

        return job_duty+job_require

    def write_item(self, list_tem):  # [{},{},...]
        str_tem = ''
        for tem in list_tem:
            job_name = tem['job_name']
            job_ty = tem['job_ty']
            job_num = tem['job_num']
            work_location = tem['work_location']
            pub_time = tem['pub_time']
            job_detail = tem['job_detail']
            str_tem = (str_tem+job_name.ljust(50-len(job_name.encode('gbk'))+len(job_name))+'\t'+
                       job_ty.center(9-len(job_ty.encode('gbk'))+len(job_ty))+'\t' +
                       job_num.center(4-len(job_num.encode('gbk'))+len(job_num))+'\t'+work_location.center(6)+
                       pub_time.center(10-len(pub_time.encode('gbk'))+len(pub_time))+'\n' +
                       job_detail+'\n')

        with open('00腾讯社招详细内容.txt'.decode('utf-8'), 'a') as f:
            f.write(str_tem.encode('utf-8'))
            f.write('\n')

if __name__ == '__main__':
    ten = Tencent()
    ten.spider()

