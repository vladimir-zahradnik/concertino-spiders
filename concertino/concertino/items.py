# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ConcertinoItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    date = Field()
    time = Field()
    place = Field()

class OpenRockItem(ConcertinoItem):
    event_url = Field()
