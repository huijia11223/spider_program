import  requests
from bs4 import BeautifulSoup
from lxml import etree
from requests.exceptions import RequestException
import csv
import scrapy

base_url="https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4"
headers={
    'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Cookie':'bid=pJjyyWPEMx8; ap=1'
}

def parse_html(html):
    # print(html)
    try:
       content=html.find_all('li',class_='subject-item')
    #    print(content)
    except:
        print("无内容")
        
    
    for book_info in content:
        atitle=book_info.select('.info h2')[0].get_text().split()

        btitle=''.join(atitle)
        pub_info=book_info.select('.info .pub')[0].get_text().strip()
        desc_list=pub_info.split()
        book_url='图书链接地址'+book_info.select('.info h2 a')[0].get('href')
        pic_url='图片链接地址'+book_info.select('.pic img')[0].get('src')
        try:
            author_info='作者/译者：'+'/'.join(desc_list[0:-3])
        except:
            author_info="无"
        
        try:
            pub_info='出版信息：'+'/'.join(desc_list[-3:])
        except:
            pub_info='无'

        try:
            rating=book_info.select('.info  .rating_nums')[0].get_text().strip()
        except:
            rating='0.0'
        
        try:
            people_num=book_info.select('.info .pl')[0].get_text().strip()

        except:
            people_num='0'
        
        yield{
            "title":btitle,
            "rating":rating,
            "people_num":people_num,
            "author_info":author_info,
            "pub_info":pub_info,
            "book_url":book_url,
            "pic_url":pic_url,
        }

    



        
    

def get_html(url):
    try:
        req=requests.get(url,headers=headers)
        if req.status_code==200:
            return BeautifulSoup(req.text,'lxml')
    except RequestException as e:
        print(e)
        return None
        
def write_csv_header(path,headers):
    with open(path,"a",encoding="utf-8",newline="") as f:
        f_csv=csv.DictWriter(f,headers)
        f_csv.writeheader()

def write_csv_rows(path,headers,rows):
    with open(path,'a',encoding="utf-8",newline="") as f:
        f_csv=csv.DictWriter(f,headers)
        f_csv.writerows(rows)

def main():
    filename="豆瓣读书1.csv"
    headers=["title","rating","people_num","author_info","pub_info","book_url","pic_url"]
    write_csv_header(filename,headers)

    html=get_html(base_url)
    items=parse_html(html)
    books=[]

    for item in items:
        books.append(item)

    write_csv_rows(filename,headers,books)

    next_url=html.select("span.next a")[0].get('href')
    url="https://book.douban.com"+next_url
    parse_html(url)




if __name__ == '__main__':
    main()