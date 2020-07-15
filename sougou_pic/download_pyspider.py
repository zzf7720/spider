import requests
from fake_useragent import UserAgent
import os
import jsonlines
from threading import Thread

class Girl_image(object):
    def __init__(self):
        self.grils_image_path = 'D:/girls/'
        self.text_path = 'girls_info.txt'
        self.ua = UserAgent()
        self.headers = {'Referer': 'http://www.girl-atlas.com/','User-Agent':self.ua.random,}
        self.create_dir()
        self.results = self.get_info()

    def get_info(self):
        with open(self.text_path, encoding='utf-8') as f:
            results = list(jsonlines.Reader(f))
            return results

    def create_dir(self):
        if not os.path.exists(self.grils_image_path):
            os.mkdir(self.grils_image_path)

    def get_detail(self,index):
        for item in self.results[index:index+151]:
            title = item.get('result').get('title')
            print('准备下载套图:', title)
            with open('title.txt', 'a', encoding='utf-8') as f:
                f.write(title)
            if title:
                detail_path = self.grils_image_path + title.strip()
                if not os.path.exists(detail_path):
                    os.mkdir(detail_path)
            else:
                detail_path = self.grils_image_path + 'others'
                if not os.path.exists(detail_path):
                    os.mkdir(detail_path)

            image_urls = item.get('result').get('image_url')
            for item in image_urls:
                title = item.split('/')[-1].split('!')[0]
                image_path = detail_path + '/' + title
                print('开始下载：', item, '\n', '路径为:', image_path)
                try:
                    r = requests.get(item, headers=self.headers)
                    if r.status_code == 200:
                        with open(image_path, 'wb') as f:
                            f.write(r.content)
                except Exception as e:
                    print('下载失败:',e.args)

    def run(self):
        for i in range(0, len(self.results) + 1, 150):
            t = Thread(target=self.get_detail,args=(i,))
            t.start()
            t.join()

if __name__ == '__main__':
    girl = Girl_image()
    girl.run()
    print('下载完成')






