import requests
import os
from hashlib import md5
from threading import Thread

params = {
'aid': '24',
'app_name':'web_search',
'offset': 0,
'format': 'json',
'keyword': '街拍',
'autoload': 'true',
'count': '20',
'en_qc': '1',
'cur_tab': '1',
'from': 'search_tab',
}
BASE_URL = 'https://www.toutiao.com/api/search/content/?'

class Toutiao(object):
    def __init__(self,params=params,url=BASE_URL):
        self.params = params
        self.url = url
        self.dir = 'toutiao_img'

    def get_page(self,page):
        self.params['offset'] = page
        try:
            response = requests.get(url=self.url,params=self.params)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(e)

    def get_images(self,json):
        if json.get('data'):
            for item in json.get('data'):
                images = {}
                images['title'] = item.get('title')
                images['image'] = item.get('large_image_url')
                yield images

    def save_to_file(self,item):
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        try:
            response = requests.get(url=item.get('image'))
            if response.status_code == 200:
                file_name = '{}/{}.{}'.format(self.dir,md5(response.content).hexdigest(),'jpg')
                if not os.path.exists(file_name):
                    with open(file_name,'wb') as f:
                        f.write(response.content)
                else:
                    print('已存在')
        except Exception as e:
            print(e)

    def run(self,page):
        json = self.get_page(page)
        for item in self.get_images(json):
            print(item)
            self.save_to_file(item)

if __name__ == '__main__':
    toutiao = Toutiao()
    groups = [x*20 for x in range(1,10)]
    for i in groups:
        t=Thread(target=toutiao.run,args=(i,))
        t.start()
        t.join()


