import requests
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool
from threading import Thread
import aiohttp
import asyncio


BASE_URL = 'https://ibaotu.com/shipin/'


class Ibaotu(object):
    def __init__(self,base_url=BASE_URL):
        self.base_url = base_url
        self.scheme = 'https:'

    async def get_page(self,url,flag=None):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
        }
        print('正在爬取'+url)
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url,headers=headers) as response:
                    if response.status == 200:
                        if flag:
                            return await response.content.read()
                        return await response.text()
                    return None
                # headers = {
                #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
                # }
                # html = requests.get(url,headers=headers)
                # if html.status_code == 200:
                #     return html
                # return None
            except Exception as e:
                print(e)

    def parse_url(self,html):
        soup = BeautifulSoup(html,'lxml')
        url_list = soup.find(class_='media-list').find_all('li')
        for item in url_list:
            url = item.find(class_='video-box').find('a')['href']
            yield url

    def parse_html(self,html):
        soup = BeautifulSoup(html,'lxml')
        video = soup.find(class_='img-wrap').find('a')['src']
        return video

    async def download(self,url):
        print('正在下载'+url)
        url = self.scheme + url
        name = url.split('/')[-1]
        result =await self.get_page(url,flag=True)
        with open('videos/'+name,'wb') as f:
            f.write(result)


    async def run(self,page):
        url = self.base_url + '7-0-0-0-0-{}.html'.format(page)
        html =await self.get_page(url)

        videos_url = self.parse_url(html)
        for url in videos_url:
            url = self.scheme + url
            response =await self.get_page(url)
            result = self.parse_html(response)
            await self.download(result)


if __name__ == '__main__':
    print('开始爬取...')
    baotu = Ibaotu()
    loop = asyncio.get_event_loop()
    tasks = [baotu.run(x) for x in range(1,4)]
    loop.run_until_complete(asyncio.wait(tasks))

    # pool = Pool()
    # groups = (list(range(1,5)))
    # pool.map(baotu.run,groups)
    # pool.close()
    # pool.join()
    # for i in range(1,5):
    #     t = Thread(target=baotu.run,args=(i,))
    #     t.start()









