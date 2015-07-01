# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from scrapy.http import Request
from datetime import datetime
from torrent_survival import *
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class CleasingPipeline(object):
    def process_item(selfself,item,spider):
        # File size unit
        digi = float(item['file_size'][:-3])
        if item['file_size'].endswith('GB'):
            item['file_size'] = digi*1024
        elif item['file_size'].endswith('KB'):
            item['file_size'] = digi*1024
        else:
            item['file_size'] = digi
        # Release time
        item['release_time'] = datetime.strptime(item['release_time'], '%y-%m-%d %H:%M')
        # additional fields: type conversion
        item['seed_num'] = int(item['seed_num'])
        item['download_num'] = int(item['download_num'])
        item['complete_num'] = int(item['complete_num'])
        return item


class StorePipeline(object):
    def open_spider(self, spider):
        before_request_handler()

    def process_item(self, item, spider):
        dic = dict(item)
        new_commit = Torrent(**dic)
        new_commit.save()

    def close_spider(self, spider):
        after_request_handler()
