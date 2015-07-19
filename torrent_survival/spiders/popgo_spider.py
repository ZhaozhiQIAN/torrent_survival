import scrapy
from torrent_survival.items import TorrentSurvivalItem
from datetime import datetime
from urlparse import urlparse
import MySQLdb
import re

class popgo_spider(scrapy.Spider):
    name = "popgo"
    # start_urls = ["http://share.popgo.org/search.php?title=darkness"]
    def start_requests(self):
        db = MySQLdb.connect(host='localhost', user='root',
                                    passwd='Windows9', db='ani_torr', charset='utf8')
        try:
            db.query("SELECT keyword FROM Anime;")
        except MySQLdb.Error, e:
            print "<selecting keyword> Error %d: %s" % (e.args[0], e.args[1])
        r=db.store_result()
        rows = r.fetch_row(maxrows=0)
        for one_kw in rows:
            one_kw = one_kw[0]
            base_query = u'http://share.popgo.org/search.php?title={kw}'
            url = base_query.format(kw = one_kw)
            yield self.make_requests_from_url(url)

    def extract_keyword(self, curr_url):
        curr_url = curr_url
        url_args = urlparse(curr_url).query.split('&')
        for arg in url_args:
            if arg.startswith('title='):
                page_keyword = arg[6:]
                # hex0 = r'(?P<hex>%[A-Fa-f0-9]{2})'
                # wd = r'(?P<wd>[A-Z]+)'
                # hex_pat = re.compile('|'.join([hex0, wd]))
                #
                # scanner = hex_pat.scanner(page_keyword)
                # tokens = []
                # for m in iter(scanner.match, None):
                #     if m.lastgroup == 'hex':
                #         hexdigi = m.group()[1:].decode('hex').decode('utf-8')
                #         tokens.append(hexdigi)
                #     else:
                #         tokens.append(m.group())
                # return u''.join(tokens)
                return page_keyword

    def parse(self,response):
        # TODO: handle "sorry no torrent found"
        main_table = response.css('#index_maintable > tbody:nth-child(1)')
        children = main_table.css('tr')
        curr_url = response.request.url
        page_keyword = self.extract_keyword(curr_url)
        crawl_next_page_flag = True
        for child in children[1:-1]:
            item = TorrentSurvivalItem()
            time = child.css("td:nth-child(2)::text").extract()
            date = child.css("td:nth-child(2)>p::text").extract()
            item["release_time"] = date[0] + ' ' + time[0]
            item['release_time'] = datetime.strptime(item['release_time'], '%y-%m-%d %H:%M')
            if item['release_time'] < datetime(2015, 7, 1):
                crawl_next_page_flag = False
                continue
            else :
                item["category"] = child.css("td:nth-child(3)::text").extract()[0]
                item["torr_name"] = child.css("td:nth-child(4)>a").xpath('@title').extract()[0]
                item["file_size"] = child.css("td:nth-child(5)::text").extract()[0]
                item["seed_num"] = child.css("td:nth-child(6)::text").extract()[0]
                item["download_num"] = child.css("td:nth-child(7)::text").extract()[0]
                item["complete_num"] = child.css("td:nth-child(8)::text").extract()[0]
                item["grab_time"] = datetime.now()
                item['keyword'] = page_keyword
                yield item
        if crawl_next_page_flag:
            max_page = response.css('#page::text').extract()[0]
            lbra = max_page.find('(')
            rbra = max_page.find(')')
            try:
                max_page = int(max_page[lbra+1: rbra])
            except ValueError:
                max_page = -1
            page_loc = curr_url.find('page=')
            if page_loc != -1:
                next_page = int(curr_url[page_loc+5:]) + 1
                next_url = curr_url[:page_loc+5] + str(next_page)
            else:
                next_page = 2
                next_url = curr_url+'&page=2'
            # print next_url
            if next_page <= max_page:
                yield self.make_requests_from_url(next_url)

        pass
