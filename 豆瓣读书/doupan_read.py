import  requests
from bs4 import BeautifulSoup
from lxml import etree
from requests.exceptions import RequestException
import csv

base_url="https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4"
headers={
    'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Cookie':'bid=pJjyyWPEMx8; ap=1'
}

def parse_html(html):
    alls=html.xpath("//div[@id='subject_list']/ul[@class='subject-list']")
    # print(alls)
    
    for all in alls:
        
        
        pubs=all.xpath("./li[@class='subject-item']/div[2]/div[@class='pub']/text()")
        # authors=[];translaters=[];producers=[];publishers=[];years=[];prices=[]
        for pub in pubs:
            titles=all.xpath("./li[@class='subject-item']/div[2]/h2/a/text()")[0].strip()
            pub1=pub.strip().split("/")
            
            # print(pub1)
            # print(len(pub1))`
            #['钱锺书 ', ' 人民文学出版社 ', ' 1991-2 ', ' 19.00']
            # 4
            # ['[美] 约翰·威廉斯 ', ' 杨向荣 ', ' 世纪文景', '上海人民出版社 ', ' 2016-1 ', ' 39.00元']
            # 6
            # ['[美] 库尔特·冯内古特 ', ' 董乐山 ', ' 百花洲文艺出版社 ', ' 2017-6 ', '38.00元']
            # 5 `
            if len(pub1)==4:
                pub1.insert(1,'null') 
                pub1.insert(2,"null")
            elif len(pub1)==5:
                pub1.insert(2,"null")
            else:
                print("有大于6个或者小于4个")
            
           
            
            yield{
                "title":titles,
                "author":pub1[0],
                "translater":pub1[1],
                "producer":pub1[2],
                "publisher":pub1[3],
                "year":pub1[4],
                "price":pub1[5],
            }

def write_csv_header(path,headers):
    with open(path,"a",encoding="utf-8",newline="") as f:
        f_csv=csv.DictWriter(f,headers)
        f_csv.writeheader()

def write_csv_rows(path,headers,rows):
    with open(path,'a',encoding="utf-8",newline="") as f:
        f_csv=csv.DictWriter(f,headers)
        f_csv.writerows(rows)
 

def get_html(url):
    try:
        req=requests.get(url,headers=headers)
        if req.status_code==200:
            return etree.HTML(req.text)
    except RequestException as e:
        print(e)
        return None
        

def main():
    filename="豆瓣读书.csv"
    headers=["title","author","translater","producer","publisher","year","price"]
    # write_csv_header(filename,headers)

    html=get_html(base_url)
    items=parse_html(html)
    books=[]

    for item in items:
        books.append(item)

    write_csv_rows(filename,headers,books)


if __name__ == '__main__':
    main()