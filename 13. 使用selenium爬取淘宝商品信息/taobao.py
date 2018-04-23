# -*- coding: utf-8 -*-
# 2018/4/22 17:26

'''
    由于PhantomJS最新版已经失效，并且作者已经放弃更新，所以决定改用无头的chrome
    需要下载chromedriver.exe，将其放到python3的安装目录下即可（添加环境变量）
'''


import pymongo
import random
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


client = pymongo.MongoClient('localhost', 27017)
mydb = client['mydb']
# 先将原来可能存在的'taobao'删除
mydb.drop_collection('taobao')
taobao = mydb['taobao']
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# chrome.exe的具体路径
chrome_options.binary_location = r'C:\Users\xxxx\AppData\Local\Google\Chrome\Application\chrome.exe'


def get_info(driver):
    while True:
        driver.get(driver.current_url)
        driver.implicitly_wait(random.randint(10, 20))
        selector = etree.HTML(driver.page_source)
        items = selector.xpath('//div[starts-with(@class, "item J_MouserOnverReq ")]')
        for item in items:
            # string(.)的用法得注意
            name = item.xpath('div[2]/div[2]/a')[0].xpath('string(.)').strip()
            price = item.xpath('div[2]/div[1]/div[1]/strong/text()')[0]
            shop = item.xpath('div[2]/div[3]/div[1]/a[1]/span[2]/text()')[0]
            location = item.xpath('div[2]/div[3]/div[2]/text()')[0]
            sell = item.xpath('div[2]/div[1]/div[2]/text()')[0]
            product = {'name': name, 'price': price, 'shop': shop, 'location': location, 'sell': sell}
            print(product)
            taobao.insert_one(product)
        try:
            # 点击下一页
            element = driver.find_element_by_xpath('//a[@trace="srp_bottom_pagedown"]')
            element.click()
            time.sleep(random.randint(2, 5))
        except NoSuchElementException:
            break


if __name__ == '__main__':
    url = 'https://www.taobao.com'
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(15)
    driver.find_element_by_id('q').clear()
    driver.find_element_by_id('q').send_keys('ikbc')
    driver.find_element_by_xpath('//button[@class="btn-search tb-bg"]').click()
    get_info(driver)
