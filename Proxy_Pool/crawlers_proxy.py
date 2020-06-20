import json
from Proxy_Pool.utils import get_page
from bs4 import BeautifulSoup

class Proxy_MetaClass(type):
    def __new__(cls, name,bases,attrs):
        count = 0
        attrs['__CrawlFunc__']=[]
        for k,v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count +=1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls,name,bases,attrs)

class Crawler(object,metaclass=Proxy_MetaClass):
    def get_proxies(self,callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理',proxy)
            proxies.append(proxy)
        # print(proxies)
        return proxies

    def crawl_daili66(self,page_count=4):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1,page_count+1)]
        for url in urls:
            print('Crawling:',url)
            html = get_page(url)
            if html:
                soup = BeautifulSoup(html,'lxml')
                trs = soup.find(class_='containerbox').table.find_all('tr')[1:]
                for tr in trs:
                    tds = tr.find_all('td')
                    ip = tds[0].string.strip()
                    port = tds[1].string.strip()
                    yield ':'.join([ip,port])

    def crawl_kuaidaili(self,page_count=5):
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling:', url)
            html = get_page(url)
            if html:
                soup = BeautifulSoup(html, 'lxml')
                trs = soup.find(class_='table-bordered').tbody.find_all('tr')
                for tr in trs:
                    tds = tr.find_all('td')
                    ip = tds[0].string.strip()
                    port = tds[1].string.strip()
                    yield ':'.join([ip, port])

    def crawl_89ip(self,page_count=5):
        start_url = 'http://www.89ip.cn/index_{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling:', url)
            html = get_page(url)
            if html:
                soup = BeautifulSoup(html, 'lxml')
                trs = soup.find(class_='layui-table').tbody.find_all('tr')
                for tr in trs:
                    tds = tr.find_all('td')
                    ip = tds[0].string
                    port = tds[1].string
                    yield ':'.join([ip.strip(), port.strip()])












