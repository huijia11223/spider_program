import requests
from bs4 import BeautifulSoup
import urllib
import re
import time
import random
import csv

def devideTag(tags):
    for tag in tags:
        tagSpider(tag)

def tagSpider(tag):
    headers={
        'Cookie':'__uuid=d0a8152b-3b7b-706e-ee7a…1@1535729497536@1534433497536',
        'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    }

    URL='http://v.iqiyi.com/index/%s/' % tag
    # print(URL)
    time.sleep(random.random()*5)

    try:
        text_one=urllib.request.urlopen(URL).read()
        # print(text_one)
    except Exception as e:
        print(e)
    
    soup=BeautifulSoup(text_one,'lxml')
    # print(soup)

    try:
        content=soup.find_all(attrs={'data-ranklist-elem':'item'})
        # print(content)

    except :
        print("没有这个标签")
    loadData(content,tag)

def loadData(content,tag):
    for node in content:
        # print(node)
        # print("*****"*10)
        keyword=node.select('.rank_list a')[0].get_text().strip()
        # print(keyword)
        info=node.select('.item_usrInfo a')[0]

        
        yester_index=node.select('td:nth-of-type(3) div span')[0].get_text().strip()
        # print(yester_index)
        week_index=node.select('td:nth-of-type(4)')[0].get_text().strip()
        # print(week_index)
        month_index=node.select('td:nth-of-type(5)')[0].get_text().strip()
        # print(month_index)
        
    #     with open('%s.txt' % tag,'a',encoding='utf-8') as f:
    #             f.write('%s  %s  %s  %s  %s  ' % (keyword,info,yester_index,week_index,month_index))
    #             f.write('\n')
    # print("success")
    #因为每个页的标签不同，所以无法抓取

def printTag():
    host="http://v.iqiyi.com/index/"
    # response=requests.get("http://v.iqiyi.com/index/")
    text=urllib.request.urlopen(host).read()
    soup=BeautifulSoup(text,'lxml')
    # print(soup.prettify())
    
    tags=soup.select('.mod_side_nav li a em')
    
    tags_list=[]
    start=0
    end=3

    for tag in tags:
        # print(tag.get_text())
        tags_list.append(tag.get_text())
    
    tags_list.pop(0)
    # print(tags_list)

    tr,td=divmod(len(tags_list),3)
    # print(tr,td)

    if td!=0:
        tr=tr+1
    for i in range(tr):
        print(tags_list[start:end])
        start,end=end,end+3
    


def main():
    tag_list=[]
    printTag()
    while True:
        inp=input("请输入要抓取的标签名的拼音:(eg:电视(dianshi))和按q退出:")
        if inp.lower()=='q':
            break
        tag_list.append(inp)
    
    devideTag(tag_list)
    



if __name__ == '__main__':
    main()