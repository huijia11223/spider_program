from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from config import *
import pymongo

brower=webdriver.PhantomJS(service_args=SERVICE_ARGS)
brower.maximize_window()
client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

#获得首页
def search():
    brower.get("https://a.jd.com/coupons.html")
    get_youhuiquan()

#提取数据
def get_youhuiquan():
    html=brower.page_source
    doc=pq(html)
    items=doc('#coupons-list .quan-item .q-type').items()

    for item in items:
        youhuiquan={
            'price':item.find('.q-price').text().replace("\n","").strip(),
            'limit':item.find('.limit').text(),
            'store':item.find('.q-range > div:nth-child(1) > p').text(),
            'time':item.find('.q-range > div:nth-child(3)').text(),
        }
        print(youhuiquan)
        save_mongo(youhuiquan)

#保存mongo
def save_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print("插入成功：",result)
    except Exception:
        print("存储失败",result)
        save_mongo(result)

#翻到下一页
def next_page(i):
    print("正在查询：",i)
    try:
        
        next_button=brower.find_element_by_css_selector("body > div.main > div > div.w > div:nth-child(2) > div > div.ui-page-wrap.clearfix.mb40 > div > a.ui-pager-next")   
        next_button.click()
        EC.text_to_be_present_in_element((By.CSS_SELECTOR,'body > div.main > div > div.w > div:nth-child(2) > div > div.ui-page-wrap.clearfix.mb40 > div > a.ui-page-curr'),str(i))
        get_youhuiquan()
        time.sleep(3)

    except TimeoutError:
        print("网页出现错误")
        next(i)
    


def main():
    try:
        search()
        for i in range(2,101):
            next_page(i)
    except Exception:
        print("出错了")
    finally:
        brower.close
    


if __name__ == '__main__':
    main()