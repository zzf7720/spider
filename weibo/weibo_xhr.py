import requests
from fake_useragent import UserAgent
from pyquery import PyQuery as pq
from pymongo import MongoClient

ua = UserAgent()
base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
    'referer':'referer',
    'User-Agent':ua.random,
}
client = MongoClient()
db = client['weibo']
collection = db['info']
count = 10

def get_page(rollback_args=None):
    params = {
        'type':'uid',
        'value': '5720474518',
        'containerid': '1076035720474518',
        'since_id': rollback_args
    }

    try:
        req = requests.get(url=base_url,params=params,headers=headers)
        if req.status_code == 200:
            return  req.json()
    except Exception as e:
        print(e)


def parse_page(json):
    if json:
        next_sinceid = json.get('data').get('cardlistInfo').get('since_id')
        items = json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            if not item:
                continue
            weibo_info = {}
            weibo_info['id'] = item.get('id')
            weibo_info['text'] = pq(item.get('text')).text()
            weibo_info['attitudes'] = item.get('attitudes_count')
            weibo_info['comments'] = item.get('comments_count')
            weibo_info['reposts'] = item.get('reposts_count')
            save_to_mongo(weibo_info)
        return next_sinceid

def save_to_mongo(result):
    if collection.insert(result):
        print('Saved to Mongo')


def run(since_id=None):
    global count
    if count:
        json = get_page(since_id)
        since_id = parse_page(json)
        run(since_id)
        count -=1

if __name__ == '__main__':
    run()

