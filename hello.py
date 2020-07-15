import requests

r = requests.get('http://stock.eastmoney.com/a/202007141553766441.html')
r.encoding = 'utf-8'
print(r.text)