# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class TuniuItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    href=Field()
    image=Field()
    title=Field()
    price=Field()
    satNum=Field()
    peopleNum=Field()
    peopleComment=Field()
    overview=Field()
    brand=Field()
    time=Field()
    subtitle=Field()
    tip=Field()

