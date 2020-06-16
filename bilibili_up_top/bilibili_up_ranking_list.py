import requests
from lxml import etree
import json

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

def parse_page(content):
    html = etree.HTML(content)
    result = html.xpath('//div[@class="ups-list"]/a')
    for item in result:
        name = (item.xpath('div//span[@class="name blue"]/text()'))[0]
        index = (item.xpath('div//span[@class="index"]/text()'))[0]
        face = (item.xpath('div//img[@class="face"]/@src'))[0]
        sign = (item.xpath('div//div[@class="sign"]/text()'))[0]
        fans = (item.xpath('div//p[contains(@class,"fans")]/text()'))[0] + html.xpath('//*[@id="app"]/div/div[3]/div[2]/a[1]/div/div[2]/div[2]/p[2]/text()')[0]
        play_num = (item.xpath('div//p[contains(@class,"playNum")]/text()'))[0] + html.xpath('//*[@id="app"]/div/div[3]/div[2]/a[1]/div/div[2]/div[3]/p[2]/text()')[0]
        total.append({
            'index':index,
            'name': name,
            'face':face,
            'sign':sign,
            'fans':fans,
            'play_num':play_num,
        })

def write_to_file(content):
    with open('bilibili_up_ranking_list.json','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False,indent=2)+'\n')

if __name__ == '__main__':
    total = []
    url = 'https://www.kanbilibili.com/rank/ups/fans'
    html = get_html_page(url)
    parse_page(html)
    for i in total:
        write_to_file(i)
    print(total)

