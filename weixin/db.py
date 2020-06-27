from pickle import dumps,loads
from weixin.request import Weixin_request
from  redis import StrictRedis
from weixin.config import *

class RedisQueue():
    def __init__(self):
        self.db = StrictRedis(host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD)

    def add(self,request):
        if isinstance(request,Weixin_request):
            return self.db.rpush(REDIS_KEY,dumps(request))
        return False

    def pop(self):
        if self.db.llen(REDIS_KEY):
            return loads(self.db.lpop(REDIS_KEY))
        else:
            return False

    def empty(self):
        return self.db.llen(REDIS_KEY) == 0







