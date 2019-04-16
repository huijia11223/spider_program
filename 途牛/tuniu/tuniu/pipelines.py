# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
from scrapy.conf import settings
import csv

class TuniuPipeline(object):
    def process_item(self, item, spider):
        return item

#JSON
class tuniuJson(object):
    def __init__(self):
        self.file=open('途牛旅行.json','w',encoding='utf-8')
    
    def process_item(self,item,spider):
        line=json.dumps(dict(item),ensure_ascii=False)+"\n"
        self.file.write(line)
        return item
    
    def spider_closed(self,spider):
        self.file.close()

# MONGO
class TuniuMongo(object):
    def __init__(self):
        self.client=pymongo.MongoClient(host=settings['MONGO_HOST'],port=settings['MONGO_PORT'])
        self.db=self.client[settings['MONGO_DB']]
        self.post=self.db[settings['MONGO_COLL']]
    
    def process_item(self,item,spider):
        postItem=dict(item)
        self.post.insert(postItem)
        return item
    
    def close_spider(self,spider):
        self.client.close()

# csv
class tuniuCsv(object):
    def __init__(self):
        self.f=open('tuniu.csv','w',encoding='utf-8')
        self.writer=csv.writer(self.f)
        self.writer.writerow(['链接','图片链接','标题','价格','人数','评论人数','景点','供应商','时间','出发地/旅行团/著名景点','标签'])
    
    def process_item(self,item,spider):

        tuniu_list=[item['href'],item['image'],item['title'],item['price'],
                        item['satNum'],item['peopleNum'],item['peopleComment'],
                        item['overview'],item['brand'],item['time'],item['subtitle'],
                        item['tip']]
        self.writer.writerow(tuniu_list)
        return item

    def close_spider(self,spider):
        self.writer.close()
        self.f.close()

   
