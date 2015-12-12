# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CateringItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    url_key = scrapy.Field()
    sku = scrapy.Field()
    accessories = scrapy.Field()
    meta_desc = scrapy.Field()
    meta_key = scrapy.Field()
    meta_title = scrapy.Field()
    brand_logo = scrapy.Field()
    thumb_src = scrapy.Field()
    thumb_alt = scrapy.Field()
    has_option = scrapy.Field()
    dropdown = scrapy.Field()
    options = scrapy.Field()
