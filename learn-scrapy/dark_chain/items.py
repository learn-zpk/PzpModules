# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class DarkChainDomainNameItem(scrapy.Item):
    domainname = scrapy.Field()
    num = scrapy.Field()
    origin_url = scrapy.Field()
    typo = scrapy.Field()
