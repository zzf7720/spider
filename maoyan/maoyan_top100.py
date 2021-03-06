import requests
import re
import json
import time
from requests.exceptions import RequestException

def get_html_page(url):
    try:
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
        }
        html = requests.get(url,headers=headers)
        if html.status_code == 200:
            return html.text
        return None
    except RequestException:
        return None


def parse_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.'
        '*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',re.S
    )
    items = re.findall(pattern,html)

    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2].strip(),
            'actor':item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time':item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score':item[5].strip() + item[6].strip()
        }

def write_to_file(content):
    with open('maoyan.json','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def main(offset):
    url = 'https://maoyan.com/board/4?offset=0'+str(offset)
    html = get_html_page(url)
    result=parse_page(html)

    for i in result:
        write_to_file(i)
    # print(html)

if __name__ == '__main__':
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)



