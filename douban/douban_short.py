'''
爬取豆瓣电影短评并生成词云
'''

import requests
from lxml import etree
import time
import random
import jieba
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from selenium import webdriver
from urllib.parse import urlencode
from snownlp import SnowNLP

session = requests.Session()
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
               "Referer": 'https://accounts.douban.com/passport/login',
               "Cookie": 'll="118277"; bid=vRPBwkuywiU; __utmz=30149280.1592054784.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _vwo_uuid_v2=D4CB7EFCAD2A6981F57818DB242559B90|bddbae10740397a76f795f3d103e9faf; ap_v=0,6.0; __utmc=30149280; __utmc=223695111; __utma=30149280.533259533.1592054784.1593823203.1593825317.17; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1593825898%2C%22https%3A%2F%2Fsearch.douban.com%2Fmovie%2Fsubject_search%3Fsearch_text%3D%25E6%2598%259F%25E9%2599%2585%25E7%25A9%25BF%25E8%25B6%258A%26cat%3D1002%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1930794854.1592054784.1593823203.1593825898.17; __utmz=223695111.1593825898.17.2.utmcsr=search.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/movie/subject_search; __utmb=223695111.0.10.1593825898; push_doumail_num=0; push_noty_num=0; __utmv=30149280.15675; dbcl2="156757378:t2ZqteGf9vA"; ck=L-JL; __utmt=1; __utmb=30149280.16.10.1593825317; _pk_id.100001.4cf6=37cf8477c7f04d72.1592054784.17.1593829930.1593823230.'
               }

def login():
    # proxies = {
    #     'http': 'http://' + get_proxy(),
    #     'https': 'https://' + get_proxy()
    # }

    r = session.get('https://movie.douban.com/', headers=headers)
    if r.status_code == 200:
        print('登入成功')

def get_proxy():
    try:
        req = requests.get('http://47.114.36.23:5555/random')
        if req.status_code == 200:
            return req.text
    except:
        return None

def spider_lianjie(lianjie,flag=None):
    f = open('result.txt', 'a+', encoding="utf-8")
    page = 0
    while page < 20:
        if flag:
            url = lianjie
        else:
            url = lianjie.split('/')[:-1] + 'comments'
        params = {
            'start': page * 20,
            'limit': 20,
            'sort': 'new_score',
            'status': 'P'
        }
        html = session.get(url=url,params=params,headers=headers)
        print(html.text)
        page +=1
        print("开始爬取第{}页{}：".format(page,'*'*50))
        print(html.url)
        tree = etree.HTML(html.text)
        comments = tree.xpath('//*[@id="comments"]/div')
        if len(comments) > 1:
            for item in comments:
                comment = item.xpath('.//span[@class="short"]/text()')
                if comment:
                    print(comment)
                    f.write(comment[0]+'\n')
            time.sleep(2)
        else:
            f.close()
            print("大约共{0}页评论".format(page - 1))
            break

def spider_name(name):
    params = urlencode({'search_text':name})
    move_url = 'https://movie.douban.com/subject_search'
    html = requests.get(url=move_url,params=params,headers=headers)
    drive = webdriver.PhantomJS()
    drive.get(html.url)
    first_result = drive.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div/div[1]/div/div[1]/a').get_attribute('href')
    move_url = first_result+ 'comments?'
    print(move_url)
    spider_lianjie(move_url,flag=True)

def spider_kind():

    kind = int(input("请选择搜索类型：1.根据电影链接 2.根据电影名："))
    if kind == 1:
        lianjie = input("请输入电影链接:")
        spider_lianjie(lianjie)
    elif kind == 2:
        name = input("请输入电影名:")
        spider_name(name)
    else:
        print("sorry,输入错误！")



def create_word_cloud():
    with open('result.txt', encoding='utf-8') as f:
        txt = f.read()
    words = jieba.lcut(txt)
    words = ' '.join(words)
    wc_mask = np.array(Image.open('20151025120451_NRnyr.png'))
    stop_words = {'还是', '不是', '可以', '自己', '因为', '觉得', '就是', '这个', '看到', '其实', '如果', '我们', '一部', '什么', '一个', '很多', '没有'}
    c = WordCloud(font_path='msyh.ttc', stopwords=stop_words, background_color='white', mask=wc_mask)
    c.generate(str(words))
    c.to_file('Cloud.png')


if __name__ == '__main__':
    login()
    spider_kind()
    create_word_cloud()