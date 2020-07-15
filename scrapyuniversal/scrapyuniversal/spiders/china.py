# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyuniversal.items import NewItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Join,Compose

class NewLoader(ItemLoader):
    default_output_processor = TakeFirst()

class ChinaLoader(NewLoader):
    text_out = Compose(Join(),lambda s:s.strip())
    source_out = Compose(Join(),lambda s:s.strip())

class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['http://tech.china.com/articles/']

    rules = (
        Rule(LinkExtractor(allow=r'article\/.*\.html',restrict_xpaths='//div[@class="wntjItem item_defaultView clearfix"]//div[@class="item-con-inner"]'),
             callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="pages"]/ul/a[last()]'))
    )

    def parse_item(self, response):
        loader = ChinaLoader(item=NewItem(),response=response)
        loader.add_xpath('title','//h1[@id="chan_newsTitle"]/text()')
        loader.add_value('url',response.url)
        loader.add_xpath('text','//div[@id="chan_newsDetail"]//text()')
        loader.add_xpath('datetime','//div[@class="chan_newsInfo_source"]/span[1]/text()',re='(\d+-\d+-\d+\s\d+:\d+:\d+)')
        loader.add_xpath('source','//div[@class="chan_newsInfo_source"]/span[2]/text()',re='来源：(.*)')
        loader.add_value('website','中华网')
        yield loader.load_item()

