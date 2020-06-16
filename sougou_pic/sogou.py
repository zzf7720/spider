from urllib.parse import urlencode
import requests
# from bs4 import BeautifulSoup


base_url = 'https://pic.sogou.com/pics/channel/getAllRecomPicByTag.jsp?category=%E5%A3%81%E7%BA%B8&tag=%E6%B8%B8%E6%88%8F&'
headers = {
            'Host':'pic.sogou.com',
            'Referer':'https://pic.sogou.com/pics/recommend?category=%B1%DA%D6%BD&from=home#%E6%B8%B8%E6%88%8F%2610',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45',
            'X-Requested-With':'XMLHttpRequest',
        }

def get_page(start):
    params = {
        'start':start,
        'len':15,
        'width':1600,
        'height':900,
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error',e.args)


def parse_page(json):
    if json:
        items = json.get('all_items')
        for item in items:
            total.append(item.get('pic_url'))

def write_to_file(url,name):
    content = requests.get(url)
    with open(name+'.jpg','wb') as f:
        f.write(content.content)


if __name__ == "__main__":
    total = []
    for start in range(4):
        json = get_page(start*15)
        parse_page(json)
    for num,i in enumerate(total):
        print('\r%{:.2f}'.format((num+1)*(100/len(total))),end='')
        name=i.split('/')[-1]
        write_to_file(i,name)



