from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from lxml import etree
import pymongo
import json


browser = webdriver.Chrome()

wait = WebDriverWait(browser,10)
KEYWORD = '小米手机'
url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)


def index_page(page):
    print('正在爬取第',page,'页')
    try:

        browser.get(url)
        if page > 1:
            input = wait.until(
                EC.presence_of_all_elements_located((By.XPATH,'//*[@id="mainsrp-pager"]/div/div/div/div[2]/input'))
            )
            submit = wait.until(
                EC.element_to_be_clickable((By.XPATH,'//*[@id="mainsrp-pager"]/div/div/div/div[2]/span[3]'))
            )
            input[0].clear()
            input[0].send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.XPATH,'//*[@id="mainsrp-pager"]/div/div/div/ul/li[contains(@class,"active")]/span'),str(page))
        )
        wait.until(
            EC.presence_of_all_elements_located((By.XPATH,'//*[@id="mainsrp-itemlist"]/div/div'))
        )
        get_products()
    except TimeoutException:
        index_page(page)


def get_products():
    html = browser.page_source
    doc = etree.HTML(html)
    items = doc.xpath('//*[@id="mainsrp-itemlist"]/div/div/div/div/div')
    for item in items:
        product = {
            'image':item.xpath('div//img[contains(@class,"J_ItemPic")]/@data-src'),
            'price':item.xpath('div//strong/text()'),
            'deal':item.xpath('div//div[@class="deal-cnt"]/text()'),
            'title':item.xpath('div//a[@class="shopname J_MouseEneterLeave J_ShopInfo"]/span[2]/text()'),
            'location':item.xpath('div//div[@class="location"]/text()'),
        }
        print(product)
        save_to_mongo(product)

MONGO_URL = 'localhost'
MONGO_DB = 'taobao_info'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def save_to_mongo(result):
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('Successful')
    except Exception:
        print('Faild')

MAX_PAGE = 3
def main():
    browser.get(url)
    with open('cookies.json','r') as f:
        cookies = json.loads(f.read())
    for i in cookies:
        browser.add_cookie(i)

    for i in range(1,MAX_PAGE+1):
        index_page(i)
    """第一次登入获取cookie并写入文件"""
    # with open('cookies.json','w') as f:
    #     f.write(json.dumps(browser.get_cookies()))


main()


