# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from scrapy.http import Request
from datetime import datetime
from torrent_survival import *
import MySQLdb
import re
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
        # additional fields: type conversion
        item['seed_num'] = int(item['seed_num'])
        item['download_num'] = int(item['download_num'])
        item['complete_num'] = int(item['complete_num'])
        return item

#
# class StorePipeline(object):
#     def open_spider(self, spider):
#         before_request_handler()
#
#     def process_item(self, item, spider):
#         dic = dict(item)
#         new_commit = Torrent(**dic)
#         new_commit.save()
#
#     def close_spider(self, spider):
#         after_request_handler()

class RecordTorrentPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost', user='root',
                                    passwd='Windows9', db='ani_torr', charset='utf8')
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        # query the existence of torrent
        try:
            base_query = u'SELECT tid FROM Torrent WHERE Torrent.torr_name = "{torr_name}";'.encode('utf-8')
            query = base_query.format(torr_name=item['torr_name'].encode('utf-8'))
            self.conn.query(query)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        r=self.conn.store_result()
        rows = r.fetch_row(maxrows=0)
        # if torrent exists: insert record
        if len(rows) != 0:
            tid = rows[0][0]
            base_insert = u"""INSERT INTO Record
            (tid, grab_time, seed_num, download_num, complete_num)
            VALUES ("{tid}", "{gt}", "{seed}", "{down}", "{comp}");"""
            this_insert = base_insert.format(tid=tid,gt=item['grab_time'],seed=item['seed_num'],
                                            down=item['download_num'],comp=item['complete_num'])
            try:
                self.cursor.execute(this_insert)
                self.conn.commit()
            except MySQLdb.Error, e:
                print "*INSERT INTO Record* Error %d: %s" % (e.args[0], e.args[1])
            raise DropItem
        # retain item for further processing
        return item

class NewRecordPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost', user='root',
                                    passwd='Windows9', db='ani_torr', charset='utf8')
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        # query the existence of Anime
        try:
            base_query = u'SELECT aid FROM Anime WHERE Anime.keyword = "{keyword}";'.encode('utf-8')
            query = base_query.format(keyword=item['keyword'].encode('utf-8'))
            self.conn.query(query)
        except MySQLdb.Error, e:
            print "*SELECT aid* Error %d: %s" % (e.args[0], e.args[1])
        r=self.conn.store_result()
        rows = r.fetch_row(maxrows=0)
        # if Anime exists
        if len(rows) != 0:
            # insert torrent
            aid = rows[0][0]
            insert_torrent = u"""INSERT INTO Torrent
            (category,torr_name,file_size,release_time,aid,source)
            VALUES ("{cat}","{tname}","{size}","{rtime}","{aid}","{source}");"""
            insert_torrent = insert_torrent.format(cat=item['category'],tname=item['torr_name'],
                                                   size=item['file_size'],rtime=item['release_time'],
                                                   aid=aid,source="popgo")
            print insert_torrent
            try:
                self.cursor.execute(insert_torrent)
                self.conn.commit()
            except MySQLdb.Error, e:
                print "*INSERT INTO Torrent* Error %d: %s" % (e.args[0], e.args[1])
            # Get Tid
            try:
                tid_query = "SELECT LAST_INSERT_ID();"
                self.conn.query(tid_query)
            except MySQLdb.Error, e:
                print "*Select updated Tid* Error %d: %s" % (e.args[0], e.args[1])
            tid_res = self.conn.store_result()
            tid = tid_res.fetch_row(maxrows=0)[0][0]
            # insert record
            base_insert = u"""INSERT INTO Record
            (tid, grab_time, seed_num, download_num, complete_num)
            VALUES ("{tid}", "{gt}", "{seed}", "{down}", "{comp}");"""
            this_insert = base_insert.format(tid=tid,gt=item['grab_time'],seed=item['seed_num'],
                                            down=item['download_num'],comp=item['complete_num'])
            try:
                self.cursor.execute(this_insert)
                self.conn.commit()
            except MySQLdb.Error, e:
                print "*INSERT INTO Record* Error %d: %s" % (e.args[0], e.args[1])
        # http://share.popgo.org/search.php?title=%E6%97%A5%E5%B8%B8%E5%A4%A7%E7%8E%8B%E3%80%91
        uni_brac = u'(?P<uni_brac>[\(\[【].+?[】\]\)])'
        # sqr_brac = r'(?P<sqr_brac>\[.+?\])'
        # round_brac = r'(?P<round_brac>\(.+?\))'
        ws = r'(?P<ws>\s+)'
        master_pat = re.compile('|'.join([uni_brac, ws]))
        # scanner = master_pat.scanner(u'【Dymy字幕組&Dymy字幕組】[悠哉日常大王Repeat_Non Non Biyori Repeat]【01】【BIG5】【1280X720】【MP4】')
        torr_name_wo_and = item['torr_name'].replace(u'&',u'][')
        torr_name_wo_and = torr_name_wo_and.replace(u'＆', u'][')
        scanner = master_pat.scanner(torr_name_wo_and)
        tokens = []
        for m in iter(scanner.match, None):
            if m.lastgroup != 'ws':
                tokens.append(m.group()[1:-1])

        query_tokens = u"('" + u"','".join(tokens) + u"')"
        # query the existence of Subgroup
        try:
            base_query = u'SELECT Subid FROM Releaser WHERE Releaser.name in {name};'.encode('utf-8')
            query = base_query.format(name=query_tokens.encode('utf-8'))

            self.conn.query(query)
        except MySQLdb.Error, e:
            print "*SELECT Subid* Error %d: %s" % (e.args[0], e.args[1])
        r=self.conn.store_result()
        rows = r.fetch_row(maxrows=0)
        # subgroup exist
        if len(rows) != 0:
            for subid in rows[0]:
                insert_upload = u"""INSERT INTO upload
                (tid, subid)
                VALUES ("{tid}","{subid}");"""
                insert_upload = insert_upload.format(tid=tid,subid=subid)
                try:
                    self.cursor.execute(insert_upload)
                    self.conn.commit()
                except MySQLdb.Error, e:
                    print "*INSERT INTO Upload* Error %d: %s" % (e.args[0], e.args[1])
        return item


class ReleaserInitPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost', user='root',
                                    passwd='Windows9', db='ani_torr', charset='utf8')
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        try:
            self.cursor.execute("""INSERT INTO Releaser (name, listed)
                        VALUES (%s, 1)""",
                       (item['name'].encode('utf-8'),))
            self.conn.commit()
        except MySQLdb.Error, e:
            print "*INSERT INTO Releaser* Error %d: %s" % (e.args[0], e.args[1])
        return item

class AnimeStorePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost', user='root',
                                    passwd='Windows9', db='ani_torr', charset='utf8')
        self.cursor = self.conn.cursor()
        now = datetime.now()
        self.now = datetime.strftime(now,'%Y-%m-%d')
    def process_item(self, item, spider):
        try:
            self.cursor.execute("""INSERT INTO Anime (title, keyword, weekday, add_date)
                        VALUES (%s,%s,%s,%s)""",
                                (item['name'], item['keyword'], item['weekday'], self.now))
            self.conn.commit()
        except MySQLdb.Error, e:
            print "*INSERT INTO Anime* Error %d: %s" % (e.args[0], e.args[1])
        return item