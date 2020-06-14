import requests
from bs4 import BeautifulSoup
import re
import json
import time

def get_html_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
        }
        html = requests.get(url,headers=headers)
        if html.status_code == 200:
            return html.text
        return None
    except:
        return None

def parse_page(html):
    soup = BeautifulSoup(html,'lxml')
    movie_list=soup.find(class_='grid_view').find_all('li')
    for item in movie_list:
        No = item.find('em').string
        image = item.find('img')['src']
        title = item.find(class_='title').string
        actor = item.find(text=re.compile('导演'))
        score = item.find(class_='rating_num').string
        try:
            quote = item.find(class_='quote').span.string
        except:
            quote = None
        yield {
            'No':No,
            'score':score,
            'title':title,
            'actor':actor.strip(),
            'quote':quote,
            'image':image,
        }

def write_to_file(content):
    with open('douban_top250','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def main(offset):
    print('\r'+f'%{(offset+25)//25*10}',end='',flush=True)
    url = 'https://movie.douban.com/top250?start=%s' % offset
    html=get_html_page(url)
    result = parse_page(html)

    for i in result:
        write_to_file(i)

if __name__ == '__main__':
    for i in range(10):
        main(i*25)
        time.sleep(1)


