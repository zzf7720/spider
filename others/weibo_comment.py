import requests
import csv
from threading import Thread
import os
from pyquery import PyQuery as pq

HEADERS= {
    'Cookie': 'WEIBOCN_FROM=1110106030; SUB=_2A25yAQRnDeRhGeBP4lsR9yjNwzmIHXVRDawvrDV6PUJbkdAKLXXFkW1NRQOdvSW8hM4psIy8EHWYIqYv0TUgSiRc; SUHB=0jBIUSxIyCgPvP; MLOGIN=1; _T_WM=97402365523; XSRF-TOKEN=dc5aee; M_WEIBOCN_PARAMS=oid%3D4422508285181410%26luicode%3D20000061%26lfid%3D4422508285181410%26uicode%3D20000061%26fid%3D4422508285181410',
    'Referer': 'https://m.weibo.cn/detail/4281013208904762',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
BASE_URL = 'https://m.weibo.cn/comments/hotflow?'
START_MID = '4422508285181410'


class Weibo_comment(object):
    def __init__(self,headers=HEADERS,base_url=BASE_URL,mid=START_MID):
        self.headers = headers
        self.base_url = base_url
        self.mid = mid
        self.path = 'comment.csv'
        self.file_header = ['name','comment','like','time']
        self.page = 10

    def get_page(self,max_id=0):
        print('max_id:',max_id)
        params = {
            'id':self.mid,
            'mid':self.mid,
        }
        if max_id:
            params['max_id'] = max_id
        print(params)
        try:
            response = requests.get(url=self.base_url,params=params,headers=self.headers)
            print(response.url)
            if response.status_code == 200:

                return response.json()
        except Exception as e:
            print(e)

    def parse_args(self,json_data):
        if json_data:
            result = json_data.get('data').get('max_id')
            return result

    def save_csv(self,json_data):
        if not os.path.exists(self.path):
            with open(self.path,'a',newline='',encoding='utf-8-sig') as f:
                write = csv.writer(f)
                write.writerow(self.file_header)


        if json_data:
            datas = json_data.get('data')
            for data in datas.get('data'):
                name = data.get('user').get('screen_name')
                comment = pq(data.get('text')).text()
                like = data.get('like_count')
                time = data.get('created_at')
                results = [name,comment,like,time]
                print(results)
                with open(self.path,'a',newline='',encoding='utf-8') as f:
                    write = csv.writer(f)
                    write.writerow(results)

    def run(self):
        mid = 0
        for _ in range(self.page):
            if not mid:
                json_data = self.get_page()
            else:
                json_data = self.get_page(max_id=mid)

            mid = self.parse_args(json_data)
            # print('mid:', mid)
            self.save_csv(json_data)

if __name__ == '__main__':
    Weibo_comment().run()







