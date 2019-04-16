# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BibiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()


    title=scrapy.Field() #房间直播标题
    username=scrapy.Field() #用户名
    peopleNumber=scrapy.Field() #观看人数
    roomId=scrapy.Field() #用户房间id
    userFace=scrapy.Field() #用户头像
    roomFace=scrapy.Field() #直播间图像
    Type=scrapy.Field() #直播类型

