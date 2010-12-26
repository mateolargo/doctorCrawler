# Scrapy settings for doclist project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
# Or you can copy and paste them from where they're defined in Scrapy:
# 
#     scrapy/conf/default_settings.py
#

BOT_NAME = 'doclist'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['doclist.spiders']
NEWSPIDER_MODULE = 'doclist.spiders'
DEFAULT_ITEM_CLASS = 'doclist.items.DoclistItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

