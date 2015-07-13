__author__ = 'steven'
import scrapy
from torrent_survival.items import ReleaserItem

class releaser_spider(scrapy.Spider):
    name = 'releaser_spider'
    start_urls = ["http://share.popgo.org/"]
    def parse(self,response):
        main_table = response.css('.group_list')
        for tr in main_table.css('tr'):
            for td in tr.css('td'):
                item = ReleaserItem()
                item['name'] = td.css('::text').extract()[0]
                yield item


