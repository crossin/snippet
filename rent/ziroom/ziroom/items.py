# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZiroomItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    location = scrapy.Field()
    region = scrapy.Field()
    prices_url = scrapy.Field()
    price = scrapy.Field()
    room_url = scrapy.Field()
    city = scrapy.Field()



