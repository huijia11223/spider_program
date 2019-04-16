import requests
import csv
from lxml import etree
from requests.exceptions import RequestException

headers={
    'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Cookie':'bid=pJjyyWPEMx8; ap=1'
}

def get_html(base_url):
    try:
        req=requests.get(base_url,headers=headers)
        if req.status_code==200:
            return etree.HTML(req.text)
        return None
    except RequestException as e:
        return None

def parse_html(html):
    contents=html.xpath("//*[@class='board-item-main']/div[@class='board-item-content']")

    for content in contents:
        title=content.xpath("./div[@class='movie-item-info']/p[@class='name']/a/text()")[0].strip()
        actor=content.xpath("./div[@class='movie-item-info']/p[@class='star']/text()")[0].replace("主演："," ").strip()
        time=content.xpath("./div[@class='movie-item-info']/p[@class='releasetime']/text()")[0].replace("上映时间："," ").strip()
        score=content.xpath("./div[2]/p/i/text()")
        score=score[0]+score[1]

        yield {
            "电影名":title,
            "主要演员":actor,
            "上映时间":time,
            "评分":score,
        }

        # print(title,actor,time,score)
def write_csv_header(path,headers):
    with open(path,"a",encoding="utf-8",newline="") as f:
        f_csv=csv.DictWriter(f,headers)
        f_csv.writeheader()
    
def write_csv_rows(path,headers,rows):
    with open(path,'a',encoding="utf-8",newline="") as f:
        f_csv=csv.DictWriter(f,headers)
        f_csv.writerows(rows)
        

def main():
    filename="猫眼.csv" #文件名
    headers=["电影名","主要演员","上映时间","评分"] #表头
    write_csv_header(filename,headers) #写入表头文件


    for page in range(0,100,10):
        jobs=[]
        base_url="http://maoyan.com/board/4?offset={}".format(page)
        # print(base_url)
        html=get_html(base_url) #解析网页
        items=parse_html(html) #获得数据

        # 下面将数据写入文件中
        for item in items:
            jobs.append(item)

        write_csv_rows(filename,headers,jobs)

if __name__ == '__main__':
    main()