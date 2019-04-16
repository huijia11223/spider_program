# -*- coding: utf-8 -*-
import scrapy
from tuniu.items import TuniuItem
from bs4 import BeautifulSoup

class TripSpider(scrapy.Spider):
    name = 'trip'
    allowed_domains = ['uniu.com']
    start_urls = ['http://www.tuniu.com/g3600/whole-gz-0/list-h0-j0_0/1']
    base_url="http://www.tuniu.com"
    

    def parse(self, response):
        soup = BeautifulSoup(response.body,'lxml')
        
        node_list=response.xpath('//*[@id="contentcontainer"]/div[2]/div[1]/div[1]/div[1]/ul/li/div/a')
        # print(node_list)

        for node in node_list:
            item=TuniuItem()

            #分析数据并爬取
            href=node.xpath('./@href').extract()
            image_url=node.xpath('./div[1]/div/img/@src').extract()
            title=node.xpath('./dl/dt/p[1]/span/@title').extract()
            tip=node.xpath('./dl/dt/p[2]//span[@class="mytip-grey"]/text()').extract()
            subtitle=node.xpath('./dl/dt/p[3]//span/text()').extract()
            view=node.xpath('./dl/dd[1]/span[2]/text()').extract()
            brand=node.xpath('./dl/dd[2]/span[1]/span/text()').extract()
            time=node.xpath('./dl/dd[2]/span[2]/span/text()').extract()
            money=node.xpath('./div[2]/div[1]/em/text()').extract()
            sat=node.xpath('./div[2]/div[2]/div[1]/span/i/text()').extract()
            people_num=node.xpath('./div[2]/div[2]/div[2]/p[1]/i/text()').extract()
            comment_people=node.xpath('./div[2]/div[2]/div[2]/p[2]/i/text()').extract()

            #整理好数据
            if len(comment_people):
                pass
            else:
                comment_people=['null']
                
            if len(tip) :
                pass
            else:
                tip=['null']
            sat=sat[0]+'%'
            
            
            #将打包好的数据返还给pipelines.py进行存储
            item['href']='http:'+''.join(href)  
            item['image']='http:'+''.join(image_url)
            item['price']='￥'+''.join(money)
            item['satNum']=sat
            item['peopleNum']=''.join(people_num)
            item['peopleComment']=''.join(comment_people)
            item['time']=''.join(time)
            item['brand']=''.join(brand)
            item['overview']=','+''.join(view)
            item['subtitle']=','+''.join(subtitle)
            item['title']=''.join(title)
            item['tip']=''.join(tip)
            
            yield item

        #下一页
        if soup.find('a',class_='page-next'):
            next_url=self.base_url+soup.find('a',class_='page-next')['href']
        
            yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)

       

        
            


            

            

