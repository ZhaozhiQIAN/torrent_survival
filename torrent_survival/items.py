# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TorrentSurvivalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    release_time = scrapy.Field()
    grab_time = scrapy.Field()
    category = scrapy.Field()
    torr_name = scrapy.Field()
    file_size = scrapy.Field()
    seed_num = scrapy.Field()
    download_num = scrapy.Field()
    complete_num = scrapy.Field()
    releaser = scrapy.Field()
    pass
