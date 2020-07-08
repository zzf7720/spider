from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

rules = {
    'china': (
        Rule(LinkExtractor(allow='article\/.*\.html',
                           restrict_xpaths='//div[@id="rank-defList"]//div[@class="item_con"]'), callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[contains(@class,"pages")]//a[contains(.,"下一页")]'))
    )
}