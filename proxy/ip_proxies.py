import requests
from bs4 import BeautifulSoup
import json

class Get_ip(object):
    '''抓取代理ip'''
    def __init__(self):
        self.url='https://www.xicidaili.com/nn/'
        self.check_url='https://www.ip.cn/'
        self.ip_list=[]

    @staticmethod
    def get_html(url):
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
        }
        try:
            r = requests.get(url=url,headers=headers)
            r.encoding='utf-8'
            html=r.text
            return html
        except Exception as e:
            return ''

    def check_ip(self,ip_address,ip_port):
        '''检测IP是否可用'''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
        }
        ip_url_next = '://'+ ip_address+':'+ip_port
        proxies={
            'http':'http'+ip_url_next,
            'https':'https'+ip_url_next,
        }
        try:
            r = requests.get(self.check_url,headers=headers,proxies=proxies,timeout=3)
            html=r.text
        except:
            print('fail-%s' % ip_address)
        else:
            print('success-%s' % ip_address)
            soup=BeautifulSoup(html,'lxml')
            div=soup.find(class_='well')
            if div:
                print(div.text)
            ip_info = {'address':ip_address,'port':ip_port}
            self.ip_list.append(ip_info)

    def main(self):
        html = self.get_html(self.url)
        soup = BeautifulSoup(html,'lxml')
        ip_list = soup.find(id='ip_list')
        ip_list = ip_list.find_all('tr')
        for ip_info in ip_list:
            td_list = ip_info.find_all('td')
            if len(td_list) > 0:
                ip_address = td_list[1].text
                ip_port = td_list[2].text
                self.check_ip(ip_address,ip_port)
        with open('ip.txt','w') as f:
            json.dump(self.ip_list,f)
        print(self.ip_list)

if __name__ == '__main__':
    get_ip = Get_ip()
    get_ip.main()










