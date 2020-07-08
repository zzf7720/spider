import json
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com/')
browser.delete_all_cookies()
with open('taobao_cookie.json','r',encoding='utf-8') as f:
    list_cookies = json.loads(f.read())

for cookie in list_cookies:
    browser.add_cookie({
        'domain': cookie['domain'],  # 此处xxx.com前，需要带点
        'name': cookie['name'],
        'value': cookie['value'],
        'path': cookie['path'],
        'expires': None
    })

browser.get("https://www.taobao.com/")