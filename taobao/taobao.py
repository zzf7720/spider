from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
import json
from lxml import etree
from pymongo import MongoClient

BASE_URL = 'https://s.taobao.com/search?q='
KEYWORD = '小米'
MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'xiaomi'
MAX_PAGE = 20

class Taobao(object):
    def __init__(self,base_url=BASE_URL,keyword=KEYWORD):
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser,10)
        self.base_url = base_url
        self.keyword = keyword
        self.url = self.base_url + quote(self.keyword)
        self.mongo = MongoClient(MONGO_URL)
        self.mongo_db = self.mongo[MONGO_DB]
        self.page = MAX_PAGE
        self.login()

    def login(self):
        self.browser.get(self.url)
        self.browser.delete_all_cookies()
        with open('taobao_cookie.json',encoding='utf-8') as f:
            cookies = json.loads(f.read())
        for cookie in cookies:
            self.browser.add_cookie({
                'domain': cookie['domain'],  # 此处xxx.com前，需要带点
                'name': cookie['name'],
                'value': cookie['value'],
                'path': cookie['path'],
                'expires': None
            })

    def index_page(self,page):
        print('正在抓取第%s页' % page)
        try:
            self.browser.get(self.url)
            if page > 1:
                input = self.wait.until(EC.presence_of_element_located((By.XPATH,'//input[@class="input J_Input"]')))
                submit = self.wait.until(EC.element_to_be_clickable((By.XPATH,'//span[@class="btn J_Submit"]')))
                input.clear()
                input.send_keys(page)
                submit.click()
            self.wait.until(EC.text_to_be_present_in_element((By.XPATH,'//li[@class="item active"]/span'),str(page)))
            self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="mainsrp-itemlist"]/div/div/div[1]/div[6]')))

        except TimeoutException:
            self.index_page(page)

    def get_products(self):
        html = self.browser.page_source
        xp = etree.HTML(html)
        items = xp.xpath('//div[@class="m-itemlist"]//div[@class="item J_MouserOnverReq  "]')
        for item in items:
            title_list = item.xpath('.//div[@class="row row-2 title"]/a/text()')
            title = ''
            for i in title_list:
                title += i.strip()
            product = {
                'image':item.xpath('.//img[@class="J_ItemPic img"]/@data-src'),
                'price':item.xpath('.//div[@class="price g_price g_price-highlight"]/strong/text()'),
                'deal':item.xpath('.//div[@class="deal-cnt"]/text()'),
                'title':title,
                'shop':item.xpath('.//a[@class="shopname J_MouseEneterLeave J_ShopInfo"]/span[2]/text()'),
                'location':item.xpath('.//div[@class="location"]/text()')
            }
            print(product)
            self.save_to_mongo(product)

    def save_to_mongo(self,result):
        try:
            if self.mongo_db[MONGO_COLLECTION].insert(result):
                print('存储到mongodb成功')
        except Exception:
            print('存储失败')

    def run(self):
        for i in range(1,self.page+1):
            self.index_page(i)
            self.get_products()




if __name__ == '__main__':
    Taobao().run()



