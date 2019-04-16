import urllib.request
import urllib.parse
import time
import ssl
import json
import pymongo
#存储
#分析评论

MONGODB_HOST="127.0.0.1"
MONGODB_PORT=27017
MONGODB_DBNAME="BIBI_COMMENTS"

host=MONGODB_HOST
port=MONGODB_PORT
dbname=MONGODB_DBNAME
client=pymongo.MongoClient(host=host,port=port)
tdb=client[dbname]
post=tdb['bibi_four']

ssl._create_default_https_context=ssl._create_unverified_context


#获取评论
def gain_comment(ids,heading):
    print(heading)
    print(ids[:4])
    ids=ids[:4]
    for id in ids:
        print("id:",id)
        comment_url="https://api.bilibili.com/x/v2/reply/cursor?access_key=5176e1cfe4d22ad34dd62177dd6cbbd6&appkey=1d8b6e7d45233436&build=5320000&mobi_app=android&oid="+str(id)+"&plat=2&platform=android&size=20&sort=0&ts=1537710630&type=1&sign=f8f6357817da73db5bfa79ea06d119e2"
        print(comment_url)
        r1=urllib.request.Request(url=comment_url,headers=headers)
        r2=urllib.request.urlopen(r1).read().decode('utf-8')
        
        comments_data=json.loads(r2)['data']['replies']
        print(comments_data)
        comments_number=json.loads(r2)['data']['cursor']['max_id']
        print(comments_number)
        

        
        if comments_number>20:
            comments_number-=20
        else:
            break
        comment_two_url="https://api.bilibili.com/x/v2/reply/cursor?access_key=5176e1cfe4d22ad34dd62177dd6cbbd6&appkey=1d8b6e7d45233436&build=5320000&max_id="+str(comments_number)+"&mobi_app=android&oid=2983740&plat=2&platform=android&size=20&sort=0&ts=1537801449&type=1&sign=c9262fdd895804f19684f162001900f1"
        print(comments_number)
        
        r1=urllib.request.Request(url=comment_two_url,headers=headers)
        r2=urllib.request.urlopen(r1).read().decode('utf-8')
        comments_data=json.loads(r2)['data']['replies']
        print(len(comments_data))
        print("******")

        # print(comments_data)
        # print(len(comments_data))
        
        # print("*******")


headers={
    'Buvid':'17888546-B1D1-47F3-AD2C-B8DFA106CEBB51784infoc',
    'User-Agent':'Mozilla/5.0 BiliDroid/5.32.0 (bbcallen@gmail.com)',
    'Device-ID':'CTFQZAFlUjYENw5oFCYUJhR1EyIVLRwuSjZSNwQ2UDUDZiZHLUMhFWcbYRF5CD5WbwM1QSNCJ14zBA',
    'Connection':'Keep-Alive',
    'Cookie':'sid=6if6p13o',
}
first_url="https://app.bilibili.com/x/v2/region/dynamic/child?access_key=5176e1cfe4d22ad34dd62177dd6cbbd6&appkey=1d8b6e7d45233436&build=5320000&channel=bilih5&mobi_app=android&platform=android&rid=32&tag_id=0&ts=1537708504&sign=c178f350e6c7924a6e454ea42144be1f"
r1=urllib.request.Request(url=first_url,headers=headers)
r2=urllib.request.urlopen(r1).read().decode('utf-8')
temp_data=json.loads(r2)['data']
# print(temp_data)

#四个推荐列表（固定的）
recommend=temp_data['recommend']
params=[]
titles=[]
for i in recommend:
    param=i['param']
    title=i['title']
    titles.append(title)
    params.append(param)
# print(titles)
# print(params)
# print(params)
# print(recommend)
# print(new)
i=0
while True:
    
    time.sleep(2)
    cbottom=temp_data['cbottom']
    new=temp_data['new']
    # print(cbottom)
    # print(new)
    
    for j in new:
        param=j['param']
        title=j['title']
        titles.append(title)
        params.append(param)
    # print("*")
    # print(params)

    print(cbottom)
    next_url="https://app.bilibili.com/x/v2/region/dynamic/child/list?access_key=5176e1cfe4d22ad34dd62177dd6cbbd6&appkey=1d8b6e7d45233436&build=5320000&ctime="+str(cbottom)+"&mobi_app=android&platform=android&pull=false&rid=32&tag_id=0&ts=1537708509&sign=3cc7bbaa7482da9879ad20c22f1e82e1"
    # print(next_url)
    r1=urllib.request.Request(url=next_url,headers=headers)
    r2=urllib.request.urlopen(r1).read().decode('utf-8')
    temp_data=json.loads(r2)['data']
    print(i)
    i+=1
    
    if i==10:
        break
print(params)
# print(len(params))

gain_comment(params,titles)
    
    # print(temp_data)
    # print(next_url)
# https://app.bilibili.com/x/v2/region/dynamic/child/list?access_key=5176e1cfe4d22ad34dd62177dd6cbbd6&appkey=1d8b6e7d45233436&build=5320000&ctime=2376023&mobi_app=android&platform=android&pull=false&rid=32&tag_id=0&ts=1537708509&sign=3cc7bbaa7482da9879ad20c22f1e82e1

#title	String	【720P】银河护卫队 动画版 (第3季)【人人影视字幕组】
# https://api.bilibili.com/x/v2/reply/cursor?access_key=5176e1cfe4d22ad34dd62177dd6cbbd6&appkey=1d8b6e7d45233436&build=5320000&mobi_app=
# android&oid=32116896&plat=2&platform=android&size=20&sort=0&ts=1537710630&type=1&sign=f8f6357817da73db5bfa79ea06d119e2

# title	String	【960P/BDRIP】高达W剧场版：无尽的华尔兹
# https://api.bilibili.com/x/v2/reply/cursor?access_key=5176e1cfe4d22ad34dd62177dd6cbbd6&appkey=1d8b6e7d45233436&build=5320000&mobi_app=android&oid=32163048&plat=2&platform=android&size=20&sort=0&ts=1537710766&type=1&sign=66e916fb957d867b13140a8da610e7f4
