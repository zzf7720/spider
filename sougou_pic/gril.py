import requests
from threading import Thread
import random
import time
import json
import queue
from lxml import etree
import os
from fake_useragent import UserAgent


class Girl(object):
    def __init__(self):
        self.start_url = 'https://www.girl-atlas.com/?p={}'
        self.base_url = 'https://www.girl-atlas.com'
        self.proxies = []
        self.ua = UserAgent()
        self.error_num = 3
        self.download_path = 'D:/girls/'
        self.page_url_queue = queue.Queue()
        self.detail_queue = queue.Queue()
        self.max_page = 250
        self.get_page_url()

    def get_page_url(self):
        for page in range(1,self.max_page+1):
            page_url = self.start_url.format(page)
            print('下发页面url', page_url)
            self.page_url_queue.put(page_url)

    def get_proxy(self):
        proxy_url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=73b1f81570704c55875c25938760707f&orderno=YZ20207101378mUFJrO&returnType=2&count=20'
        count = 0
        while count < 30:
            try:
                html = requests.get(url=proxy_url)
                if html.status_code == 200:
                    result = json.loads(html.text)
                    result = result.get('RESULT')
                    if len(self.proxies) > 5:
                        self.proxies = self.proxies[-5:]
                    for i in result:
                        print(i)
                        self.proxies.append(i.get('ip') + ':' + i.get('port'))
            except Exception as e:
                print(e)

            time.sleep(10 * 60)
            count += 1


    def get_page(self,url):
        time.sleep(1.1)
        headers = {
            'Referer': 'http://www.girl-atlas.com/',
            'User-Agent': self.ua.random
        }
        # proxy = random.choice(self.proxies)
        # proxies = {
        #     'http':'http'+proxy,
        #     'https':'https'+proxy,
        # }
        # print('使用代理:',proxy)
        try:
            # response = requests.get(url=url,headers=headers,proxies=proxies)
            response = requests.get(url=url, headers=headers)
            if response.status_code == 200:
                self.error_num = 0
                return response
            else:
                print('状态码错误', response.status_code)
                raise ConnectionError
        except:
            print('请求错误：',url)
            self.error_num -= 1
            if self.error_num:
                self.get_page(url)

    def get_detail_url(self):
        while True:
            url = self.page_url_queue.get()
            print('获取详情页：',url)
            html = self.get_page(url)
            if html:
                page = etree.HTML(html.text)
                items = page.xpath('//div[@class="album-item row"]//h2/a/@href')
                for item in items:
                    detail_url = self.base_url+item
                    self.detail_queue.put(detail_url)
            self.page_url_queue.task_done()

    def download_image(self):
        while True:
            url = self.detail_queue.get()
            print('开始下载套图:',url)
            html = self.get_page(url)
            if html:
                page = etree.HTML(html.text)
                title = page.xpath('//div[@class="header-right clearfix"]/h3/text()')[0]
                for i in ['/','"','|','\\',':','*','?','<','>']:
                    title = title.replace(i,'')
                dir = self.download_path + title.strip()
                if not os.path.exists(dir):
                    os.mkdir(dir)
                items = page.xpath('//div[@class="slideview-container"]/ul/li/img/@src')
                for item in items:
                    item = item.replace('https','http')
                    path = dir + '/' + item.split('/')[-1].split('!')[0]
                    print(path)
                    if not os.path.exists(path):
                        result = self.get_page(item)
                        print('开始下载',result.url)
                        if result:
                            try:
                                with open(path,'wb') as f:
                                    f.write(result.content)
                            except Exception as e:
                                print('下载错误:',e)

            self.detail_queue.task_done()

    def run(self):
        threading_list = []
        for _ in range(4):
            get_detail_url = Thread(target=self.get_detail_url)
            threading_list.append(get_detail_url)

        for _ in range(6):
            download_url = Thread(target=self.download_image)
            threading_list.append(download_url)

        # t1 = Thread(target=self.get_proxy)
        # t1.setDaemon(True)
        # t1.start()
        # time.sleep(3)

        for t in threading_list:
            t.setDaemon(True)
            t.start()

        for q in [self.page_url_queue,self.detail_queue]:
            q.join()


if __name__ == '__main__':
    Girl().run()

    print('爬取完成')




