# -*- coding: utf-8 -*-

# Scrapy settings for torrent_survival project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'torrent_survival'

SPIDER_MODULES = ['torrent_survival.spiders']
NEWSPIDER_MODULE = 'torrent_survival.spiders'

ITEM_PIPELINES = {
    'torrent_survival.pipelines.CleasingPipeline': 300,
    'torrent_survival.pipelines.StorePipeline': 800,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'torrent_survival (+http://www.yourdomain.com)'
