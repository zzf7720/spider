import requests
from lxml import etree
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
        }
r = requests.get('https://www.kanbilibili.com/rank/ups/fans',headers=headers)
html = etree.HTML(r.text)
result = html.xpath('//div[@class="ups-list"]/a')
# print(result)
ls=[]
for i in result:
    s=(i.xpath('div//p[contains(@class,"playNum")]/text()'))[0] + html.xpath('//*[@id="app"]/div/div[3]/div[2]/a[1]/div/div[2]/div[3]/p[2]/text()')[0]
    ls.append(s)
print(ls)
# result = html.xpath('//*[@id="app"]/div/div[3]/div[2]//div/div[1]/span[1]/text()')
# print(result)
# //*[@id="app"]/div/div[3]/div[2]/a[1]/div/div[1]/span[1]
# //*[@id="app"]/div/div[3]/div[2]/a[2]/div/div[1]/span[1]



