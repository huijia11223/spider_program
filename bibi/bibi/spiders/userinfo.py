# -*- coding: utf-8 -*-
import scrapy
import json
from bibi.items import  BibiItem

class UserinfoSpider(scrapy.Spider):
    name = 'userinfo'
    allowed_domains = ['live.bilibili.com']
    start_urls = ['https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=2&cate_id=0&area_id=0&sort_type=online&page={}&page_size=30'.format(n) 
    for n in range(1,20)]

    def parse(self, response):
        # print(response.text)
        data=response.text
        jsondata=json.loads(data,encoding='utf-8')
        # print(jsondata)
        itemsinfo=jsondata['data']
        for pinfo in itemsinfo:

            item=BibiItem()

            username=pinfo['uname']
            roodid=pinfo['roomid']
            number=pinfo['online']
            room_image=pinfo['user_cover']
            user_image=pinfo['face']
            type=pinfo['area_name']
            title=pinfo['title']

      
            item['title']=title
            item['username']=username
            item['peopleNumber']=number
            item['roomId']=roodid
            item['userFace']=user_image
            item['roomFace']=room_image
            item['Type']=type

            yield item
            

            
            
            