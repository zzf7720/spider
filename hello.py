import re

content1 = '2019-2-8 23:55'
content2 = '2020-12-3 14:88'
pattern = re.compile(r'\d{2}:\d{2}')
result = re.sub(pattern,'',content1)
print(result)
