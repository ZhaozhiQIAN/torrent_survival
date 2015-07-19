__author__ = 'steven'
import scrapy
from torrent_survival.items import AnimeItem
import json

class anime_spider(scrapy.Spider):
    name = 'anime_spider'
    start_urls = ["http://share.popgo.org/bangumi.php"]
    def parse(self, response):
        body = json.loads(response.body)
        weekdays = [u'0', u'1', u'2', u'3', u'4', u'5', u'6']
        for day in weekdays:
            ani_day = body[day]
            for ani in ani_day:
                item = AnimeItem()
                item['keyword'] = ani[u'key_word']
                item['name'] = ani[u'title']
                item['weekday'] = day
                yield item
