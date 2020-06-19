from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from lxml import etree
import pymongo



browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
KETWORD = 'ipad'
base_url = 'https://www.amazon.cn/s?k=' +quote(KETWORD)
flag = True
client = pymongo.MongoClient(host='localhost')
db = client['my_db']
collection = 'col'
real_url = 'https://www.amazon.cn'
flag = True

def get_page(url):
    full_url = real_url + url
    global flag

    try:
        if flag:
            print('start %s' % base_url)
            browser.get(base_url)
            flag = False
        else:
            print('start %s' % full_url)
            browser.get(full_url)
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div[49]/span/div/div/ul/li[@class="a-last"]/a')))
        wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]')))
        get_products()
    except TimeoutException:
        print('timeout')

def get_products():
    page = 1
    html = browser.page_source
    doc = etree.HTML(html)
    items = doc.xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div')
    for i in items:
        product = {
            'image':i.xpath('.//div[contains(@class,"s-image-square-aspect")]/img/@src'),
            'title':i.xpath('.//span[contains(@class,"a-text-normal")]/text()'),
            'price':i.xpath('.//span[@class="a-price-whole"]/text()'),
            'auto':i.xpath('.//span[@class="a-color-secondary"]/text()'),

        }
        print(product)
        save_to_mongo(product)
    url = doc.xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div[49]/span/div/div/ul/li[@class="a-last"]/a/@href')[0]
    print(url)
    if page <= 10:
        get_page(url)
        page +=1

def save_to_mongo(product):
    try:
        if db[collection].insert(product):
            print('Successful')
    except:
        print('save to mongo Falid')

def main():
    get_page(base_url)

main()










