import urllib.request
import urllib.parse

def getHeaders(temp_data=""):
    headers={
        'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
        # Accept-Encoding':'gzip, deflate, br
        # Accept-Language':'zh-CN,zh;q=0.9
        # 'Connection': 'keep-alive',
        'Cookie':'ll="118295"; bid=3sMYdqME1sE; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1539585840%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dk0NFhpYoUbb8CteUOrJy4bcCebFQavpGdS5nmClfZle9G3i72DCyNJRv4jtbJy3R%26wd%3D%26eqid%3Db57ccedf0001ed13000000065bc4371e%22%5D; _pk_id.100001.8cb4=6945d6e60e049e92.1539585840.1.1539585840.1539585840.; _pk_ses.100001.8cb4=*; __utma=30149280.1336751328.1539585841.1539585841.1539585841.1; __utmc=30149280; __utmz=30149280.1539585841.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=30149280.1.10.1539585841',
        'Host':'www.douban.com',
        'Referer':'https://www.douban.com/',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    return headers

image_pic = "https://www.douban.com/misc/captcha?id=Zv0K7v3wUJbH8iWM7Y3a0eLP:en&size=s"
req=urllib.request.Request(url=image_pic,headers=getHeaders())
image_data=urllib.request.urlopen(req)

with open("doupanverity.png","wb") as f:
    f.write(image_data.read())

verify=input("please input verify")

port_url = "https://accounts.douban.com/login"

post_data={
    'source':'None',
    'redir':'https://www.douban.com/',
    'form_email':'17876783627',
    'form_password':'hellohi123',
    'captcha-solution':verify,
    'captcha-id':'7jbHyGkPnf0cO17TTmefn4iR:en',
    'login':'登录',
}

print(urllib.request.urlopen(urllib.request.Request(url=port_url,data=urllib.parse.urlencode(post_data).encode('utf-8'),headers=getHeaders(image_data.headers['Set-Cookie']))).read().decode('utf-8'))
