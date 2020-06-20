from Proxy_Pool.db import Redis_Client
from Proxy_Pool.crawlers_proxy import Crawler

POOL_UPPER_THRESHOLD = 10000

class Getter():
    def __init__(self):
        self.redis = Redis_Client()
        self.crawler = Crawler()

    def is_over_threshold(self):
        return self.redis.count() >= POOL_UPPER_THRESHOLD

    def run(self):
        print('获取模块开始执行')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                # print(proxies)
                for proxy in proxies:
                    self.redis.add(proxy)



