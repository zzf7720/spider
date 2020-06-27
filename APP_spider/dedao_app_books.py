import json
from mitmproxy import ctx
import pymongo

client = pymongo.MongoClient('localhost')
db = client['igetget']
collection = db['books']


def response(flow):
    global collection
    url = 'https://entree-ws.igetget.com/cornflower/v1/operation/rank/get'

    if flow.request.url.startswith(url):
        text = flow.response.text
        data = json.loads(text)
        books = data.get('c').get('list')[0].get('list')
        for book in books:
            data = {

                'title': book.get('title'),
                'img': book.get('index_img'),
                'intro': book.get('intro'),
                'price': book.get('cost_intro').get('price'),

            }
            ctx.log.info(str(data))
            collection.insert(data)
