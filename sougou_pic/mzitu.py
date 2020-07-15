import requests
import queue
from lxml import etree
from threading import Thread
import time
import random
import json
from fake_useragent import UserAgent



class Mzitu(object):
    def __init__(self):
        self.base_url = 'https://www.mzitu.com/page/{}'
        self.page_url_queue = queue.Queue()
        self.detail_url_queue = queue.Queue()
        self.save_queue = queue.Queue()
        self.page = 250
        self.ua = UserAgent()
        self.error_num = 3
        self.title_path = 'C:\\Users\\zzf\\Desktop\\spider\\title.txt'
        self.image_path = "D:/mzitu/"
        self.proxies = []
        self.get_page_url()

    def get_proxies(self):
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
                    print('Proxies:',)
                    for i in result:
                        print(i)
                        self.proxies.append(i.get('ip') + ':' + i.get('port'))
            except Exception as e:
                print(e)

            time.sleep(10*60)
            count +=1


    def get_page_url(self):
        for page in range(1,self.page+1):
            page_url = self.base_url.format(page)
            print('下发页面url', page_url)
            self.page_url_queue.put(page_url)

    def get_page(self,url):
        # time.sleep(random.uniform(5,10))
        HEADERS = {
            'X-Requested-With': 'XMLHttpRequest',
            'accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange; = b3;q = 0.9',
            'cookie': 'Hm_lvt_cb7f29be3c304cd3bb0c65a4faa96c30 = 1594343516, 1594343631, 1594343775, 1594429085;views = 11;Hm_lpvt_cb7f29be3c304cd3bb0c65a4faa96c30 = 1594431969',
            'User-Agent': self.ua.random,
            'Referer': 'http://www.mzitu.com'
        }

        proxy = random.choice(self.proxies)
        proxies = {
            'http':'http://' + proxy,
            'https':'https://' + proxy,
        }
        print(proxy)
        try:
            response = requests.get(url=url,headers=HEADERS,proxies=proxies)
            if response.status_code == 200:
                self.error_num = 0
                return response
            else:
                print('状态码错误',response.status_code)
                raise ConnectionError
        except Exception as e:
            print('请求错误：',url,'\n',e)
            time.sleep(1.5)
            self.error_num -=1
            if self.error_num:
                self.get_page(url)

    def get_detail_url(self):
        while True:
            page_url = self.page_url_queue.get()
            print('获取详情页:',page_url)
            response = self.get_page(page_url)
            if response:
                html = etree.HTML(response.text)
                items = html.xpath('//ul[@id="pins"]/li/a/@href')
                for item in items:
                    self.detail_url_queue.put(item)
            self.page_url_queue.task_done()

    def get_download_url(self):
        while True:
            url = self.detail_url_queue.get()
            print('获取图片链接',url)
            response = self.get_page(url)
            if response:
                html = etree.HTML(response.text)

                next_url = html.xpath('//div[@class="pagenavi"]/a[last()]/@href')
                if next_url:
                    next_url = next_url[0]
                    print('next_url:',next_url)
                    self.detail_url_queue.put(next_url)
                img_url = html.xpath('/html/body/div[2]/div[1]/div[3]/p/a/img/@src')
                if img_url:
                    img_url = img_url[0]
                    print('img_url:',img_url)
                    self.save_queue.put(img_url)
                title = html.xpath('/html/body/div[2]/div[1]/h2/text()')
                if title:
                    title = title[0]
                    self.save_title(title)
            self.detail_url_queue.task_done()

    def save_title(self,title):
        print('title:', title)
        with open(self.title_path,'a',encoding='utf-8') as f:
            f.write(title+'\n')

    def save_img(self):
        while True:
            url = self.save_queue.get()
            print('保存图片:',url)
            file_path = self.image_path + url.split('/')[-1]
            response = self.get_page(url)
            if response:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            self.save_queue.task_done()

    def run(self):
        thread_list = []
        for _ in range(2):
            get_detail_url = Thread(target=self.get_detail_url)
            thread_list.append(get_detail_url)

        for _ in range(4):
            get_download_url = Thread(target=self.get_download_url)
            thread_list.append(get_download_url)

        for _ in range(2):
            save_img = Thread(target=self.save_img)
            thread_list.append(save_img)

        t1 = Thread(target=self.get_proxies)
        t1.setDaemon(True)
        t1.start()
        time.sleep(3)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for q in [self.page_url_queue,self.detail_url_queue,self.save_queue]:
            q.join()


if __name__ == '__main__':
    Mzitu().run()

    print('爬取完成')



