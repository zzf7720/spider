import requests
from requests.exceptions import RequestException

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
        }

def get_page(url):
    try:
        html = requests.get(url,headers=headers)
        if html.status_code == 200:
            return html.text
        return None
    except RequestException:
        return None
