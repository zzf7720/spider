import requests
from bs4 import BeautifulSoup
from multiprocessing import pool,cpu_count

def get_html_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
        }
        html = requests.get(url,headers=headers)
        if html.status_code == 200:
            return html
        return None
    except:
        return None

def parse_page(content):
    soup = BeautifulSoup(content,'lxml')
    items = soup.find(class_='list').find_all('li')
    for item in items:
        url = item.find('a')['href']
        total.append(base_url+url)

def parse_pic(content):
    soup_1 = BeautifulSoup(content, 'lxml')
    url = soup_1.find(class_='endpage').find('img')['src']
    pic.append(url)

def write_to_file(url,name):
    path = '唯美壁纸/%s' % name
    content = requests.get(url)
    with open(path,'wb') as f:
        f.write(content.content)

def main(offset):
    global base_url
    global total
    global pic
    base_url = 'http://www.netbian.com'
    pic = []
    total = []
    if offset == 1:
        url = base_url + '/weimei'
    else:
        url = base_url + '/weimei' + '/index_{}.htm'.format(offset)
    html = get_html_page(url)
    if html:
        parse_page(html.text)

    for i in total:
        html=get_html_page(i)
        if html:
            parse_pic(html.text)
    print('正在下载。。。')

    for num,i in enumerate(pic):
        print('\r%{:.2f}'.format((num+1)*(100/len(pic))),end='')
        name = i.split('/')[-1]
        write_to_file(i,name)

if __name__ == "__main__":
    print('开始爬取。。。')
    pool = pool.Pool(cpu_count())
    groups = ([x for x in range(1,20)])
    pool.map(main,groups)
    pool.close()
    pool.join()

