# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def main():
    driver_tem = webdriver.PhantomJS()
    driver_tem.get('http://www.douban.com')
    # 截屏，以看清楚验证码
    driver_tem.save_screenshot('douban.png')
    # 输入账号
    driver_tem.find_element_by_name('form_email').send_keys('18972997791')
    # 输入密码
    driver_tem.find_element_by_name('form_password').send_keys('liu189')
    # 输入验证码
    captcha = raw_input('请输入验证码:')
    driver_tem.find_element_by_id('captcha_field').send_keys(captcha)
    # 点击登录按钮
    driver_tem.find_element_by_class_name('bn-submit').click()

    # 登录后等待5秒加载网页
    time.sleep('5')
    driver_tem.save_screenshot('login.png')

    with open('douban.html', 'w') as f:
        f.write(driver_tem.page_source)

    driver_tem.quit()  # 关闭浏览器


if __name__ == '__main__':
    main()
