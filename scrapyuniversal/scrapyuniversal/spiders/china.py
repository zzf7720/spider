# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Join,Compose
from scrapyuniversal.items import NewsItem
from scrapyuniversal.loaders import *


class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['https://tech.china.com/articles/']

    rules = (
        Rule(LinkExtractor(allow='article\/.*\.html',restrict_xpaths='//div[@id="rank-defList"]//div[@class="item_con"]'), callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[contains(@class,"pages")]//a[contains(.,"下一页")]'))
    )

    def parse_item(self, response):
        loader = ChinaLoader(item=NewsItem(),response=response)
        loader.add_xpath('title','//h1[@id="chan_newsTitle"]/text()')
        loader.add_value('url',response.url)
        loader.add_xpath('text','//div[@id="chan_newsDetail"]//text()')
        loader.add_xpath('datetime','//div[@class="chan_newsInfo_source"]/span[1]/text()')
        loader.add_xpath('source','//div[@class="chan_newsInfo_source"]/span[2]/text()',re='来源：(.*)')
        loader.add_value('website','中华网')
        yield loader.load_item()



class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ChinaLoader(NewsLoader):
    text_out = Compose(Join(),lambda s:s.strip())
    source_out = Compose(Join(),lambda s:s.strip())