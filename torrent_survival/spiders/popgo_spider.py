import scrapy
from torrent_survival.items import TorrentSurvivalItem
from datetime import datetime

class popgo_spider(scrapy.Spider):
    name = "popgo"
    start_urls = ["http://share.popgo.org/"]
    def parse(self,response):
        main_table = response.css('#index_maintable > tbody:nth-child(1)')
        children = main_table.css('tr')
        for child in children[1:-1]:
            item = TorrentSurvivalItem()
            time = child.css("td:nth-child(2)::text").extract()
            date = child.css("td:nth-child(2)>p::text").extract()
            item["release_time"] = date[0] + ' ' + time[0]
            item["category"] = child.css("td:nth-child(3)::text").extract()[0]
            item["torr_name"] = child.css("td:nth-child(4)>a").xpath('@title').extract()[0]
            item["file_size"] = child.css("td:nth-child(5)::text").extract()[0]
            item["seed_num"] = child.css("td:nth-child(6)::text").extract()[0]
            item["download_num"] = child.css("td:nth-child(7)::text").extract()[0]
            item["complete_num"] = child.css("td:nth-child(8)::text").extract()[0]
            # item["releaser"] = child.css("td:nth-child(9)>a").xpath('@title').extract()[0]
            item["releaser"] = child.css("td:nth-child(9)>a::text").extract()[0]
            item["grab_time"] = datetime.now()
            yield item
            
        pass
