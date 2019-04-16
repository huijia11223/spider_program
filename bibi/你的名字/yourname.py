import urllib.request
import urllib.parse
import json
import ssl
import pymongo
ssl._create_default_https_context = ssl._create_unverified_context

MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_DBNAME = "yourname"

host = MONGODB_HOST
port = MONGODB_PORT
dbname = MONGODB_DBNAME
client = pymongo.MongoClient(host=host, port=port)
tdb = client[dbname]
post = tdb['yname']

headers = {
    'Buvid': '17888546-B1D1-47F3-AD2C-B8DFA106CEBB51784infoc',
    'User-Agent': 'Mozilla/5.0 BiliDroid/5.32.0 (bbcallen@gmail.com)',
    'Device-ID': 'CTFQZAFlUjYENw5oFCYUJhR1EyIVLRwuSjZSNwQ2UDUDZiZHLUMhFWcbYRF5CD5WbwM1QSNCJ14zBA',
    'Connection': 'Keep-Alive',
    'Cookie': 'sid = bpkd6k1d',
}

first_url = "https://api.bilibili.com/x/v2/reply/cursor?access_key=5176e1cfe4d22ad34dd62177dd6cbbd6&appkey=1d8b6e7d45233436&build=5320000&mobi_app=android&oid=13662970&plat=2&platform=android&size=20&sort=0&ts=1539411134&type=1&sign=de951929605dec51b1bbbd266fb2396b"

req=urllib.request.Request(url=first_url,headers=headers)
res=urllib.request.urlopen(req).read().decode('utf-8')
temp_data=json.loads(res)['data']

post.insert(temp_data['replies'])
    
maxid=temp_data['cursor']['max_id']
minid=temp_data['cursor']['min_id']
# print(maxid,minid)
while True:
    second_url = "https://api.bilibili.com/x/v2/reply/cursor?access_key=5176e1cfe4d22ad34dd62177dd6cbbd6&appkey=1d8b6e7d45233436&build=5320000&max_id="+str(minid-1)+"&mobi_app=android&oid=13662970&plat=2&platform=android&size=20&sort=0&ts=1539411161&type=1&sign=00bbcd491fa4b2664b82bff54267d5f8"
    # print(second_url)
    req = urllib.request.Request(url=second_url, headers=headers)
    res = urllib.request.urlopen(req).read().decode('utf-8')
    temp_data = json.loads(res)['data']

    # print(len(temp_data))
    for eve_data in temp_data['replies']:
        # print(len(temp_data['replies']))
        
        post.insert(eve_data)

    minid = temp_data['cursor']['min_id']
    # print("1:",minid)
    # print(minid)
    if minid<0:

        break
    

