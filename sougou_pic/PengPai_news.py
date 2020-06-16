from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
import os
from hashlib import md5
from multiprocessing.pool import Pool


def get_page(offset):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
    }
    params = {
        'pageidx':offset
    }
    url = 'https://www.thepaper.cn/load_index.jsp?nodeids=25462,25488,25489,25490,25423,25426,25424,25463,25491,25428,68750,27604,25464,25425,25429,25481,25430,25678,25427,25422,25487,25634,25635,25600,&channelID=25950&topCids=,7851475,7861324,7851571,7853444,7851185,7851494,7853559' + urlencode(params)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
    except:
        return None

def parse_page(content):
    soup = BeautifulSoup(content,'lxml')
    for i in soup.find_all(class_='news_li'):
        url = i.find('img')['src']
        yield url

def save_img(item):
    if not os.path.exists('test'):
        os.mkdir('test')
    try:
        response = requests.get(item)
        if response.status_code == 200:
            path = '{}/{}{}'.format('test',md5(response.content).hexdigest(),'.jpg')
            if not os.path.exists(path):
                with open(path,'wb') as f:
                    f.write(response.content)
            else:
                print('Already Download',path)
    except requests.ConnectionError:
        print('Failed to save image')


def main(offset):
    content = get_page(offset)
    for item in parse_page(content):
        print(item)
        save_img(item)

if __name__ == '__main__':
    pool = Pool()
    groups = (list(range(1,20)))
    pool.map(main,groups)
    pool.close()
    pool.join()





