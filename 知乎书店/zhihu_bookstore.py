import requests
from lxml import etree
from requests.exceptions import RequestException
import csv

# https://www.zhihu.com/api/v3/books/categories/147?version=v2&limit=5&sort_by=read_count_7days&offset=5
headers={
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': '_zap=4d320cf8-0e44-493b-94db-8d14249f5bd4; _xsrf=SiZUHNPtPiGlRvc6sCj2Lid9CBHms7OF; d_c0="AFAkcy9vKg6PTrQV_SzCZMkrvvcsSbDM0Gw=|1536145887"; q_c1=7b6c590408af44b8b4b1f5ae142a24a2|1536146175000|1536146175000; tgw_l7_route=69f52e0ac392bb43ffb22fc18a173ee6; capsion_ticket="2|1:0|10:1536152892|14:capsion_ticket|44:NjcyYWE2ZDQ1MDViNGVjZjhkZTYwOTJhNzg3ZTJmMmQ=|c2a0f151bc07388cba8fade0dda7a29a9ada1d50a664398ea4bbb14cf2eedc47"; z_c0="2|1:0|10:1536152899|4:z_c0|92:Mi4xbGxDLUJ3QUFBQUFBVUNSekwyOHFEaVlBQUFCZ0FsVk5ReU45WEFBMWdWcUxrVTRMcXAxR0hUMmM4am80NFYyd1hB|6047e629d40ce5791cc0430b2733a5dc767e46b0fd85ed36485cf0f9c92eaa8d"',
    # 'if-none-match: "c7ea173766ba1e0a9b6357e04cf19aba98263756"
    'referer': 'https://www.zhihu.com/pub/',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'x-requested-with': 'Fetch'
}

def parse_html(data):
    # jsondata=json
    # print(data)
 
    itemsinfo=data['data']
    # print(itemsi?nfo)

    for pinfo in itemsinfo:
        # print(pinfo)
        id=pinfo['id']
        des=pinfo['description']
        title=pinfo['title']
        url=pinfo['url']
        book_size=pinfo['book_size']
        score=pinfo['score']
        picture=pinfo['cover']

        authors_name=[]
        for author in pinfo['authors']:
            
            author_name=author['name']
            authors_name.append(author_name)
        # print(authors_name)

        price=pinfo['promotion']['price']
        # print(price)
        yield{
            "ID":id,
            "描述":des,
            "标题":title,
            "地址":url,
            "书本字数":book_size,
            "评分":score,
            "图片":picture,
            "作者":authors_name,
            "价格":price,

        }

def get_html(url):
    try:
        req=requests.get(url,headers=headers)
        
        if req.status_code==200:
            # print("******")
            return req.json()
        return None
    except RequestException as e:
        return None
        
def write_csv_header(file,headers):
    with open(file,'a',encoding='utf-8',newline='') as f:
        f_csv=csv.DictWriter(f,headers)
        f_csv.writeheader()

def write_csv_rows(path,headers,rows):
    with open(path,'a',encoding='utf-8',newline='') as f:
        f_csv=csv.DictWriter(f,headers)
        f_csv.writerows(rows)

def main():
    filename="知乎书店.csv"
    headers=['ID','描述','标题','地址','书本字数','评分','图片','作者','价格']
    write_csv_header(filename,headers)

    for book in range(5,100,5):
        books=[]
        base_url="https://www.zhihu.com/api/v3/books/categories/147?version=v2&limit=5&sort_by=read_count_7days&offset={}".format(book)
        # print(base_url)
        content=get_html(base_url)
        # print(content)
        items=parse_html(content)
        # print(items)
        for item in items:
            books.append(item)
        write_csv_rows(filename,headers,books)
        # print(content['data'])
# [{'is_own': False, 'type': 'ebook', 'description': '愿你有所爱 ～', 'title': '人间情爱（2017 知乎日报故事精选）', 'url': 'https://www.zhihu.com/pub/book/119560601', 'cover': 'https://pic2.zhimg.com/v2-911cbb9354eff6a43c06faf21c1b5fd9_xld.jpg', 'book_size': 132766, 'id': 119560601, 'score': 9.1,'authors': [{'avatar_url': 'https://pic4.zhimg.com/50/v2-3b1f2e192ac6d2ee0af97b46bc564200_qhd.jpg', 'name': '真实故事计划', 'url': 'https://www.zhihu.com/org/zhen-shi-gu-shi-ji-hua', 'gender': -1, 'type': 'zhihu_author', 'id': 'dd00a1331c92c5f94e28c007443271b5'}, {'avatar_url': 'https://pic1.zhimg.com/50/f868d5906758ca93a54af03940fccee0_qhd.jpg', 'name': 'TNT TNT', 'url': 'https://www.zhihu.com/people/tnttnt', 'gender': -1, 'type': 'zhihu_author', 'id': 'bcb53e9eb29689b4c52fba7689f07349'}, {'avatar_url': 'https://pic4.zhimg.com/50/v2-fb2780ba0abd9ffe36bb7f43c99a884e_qhd.jpg', 'name': '马拓', 'url': 'https://www.zhihu.com/people/ma-tuo-82', 'gender': -1, 'type': 'zhihu_author', 'id': 'f002c59c3819179cf5c2a3a8928d8010'}, {'avatar_url': 'https://pic4.zhimg.com/50/19883577d_qhd.jpg', 'name': '胡微', 'url':'https://www.zhihu.com/people/hu-wei-20-12', 'gender': -1, 'type': 'zhihu_author', 'id': '88e37951307f3d09bd65924b621caa6d'}, {'avatar_url': 'https://pic2.zhimg.com/50/v2-d01f122efea768ef8ef7560db5cce968_qhd.jpg', 'name':'pm0238', 'url': 'https://www.zhihu.com/people/pm0238', 'gender': 1, 'type': 'zhihu_author', 'id': '22306976c4ae47a5fb2b9c9dcdf26f74'}, {'avatar_url': 'https://pic4.zhimg.com/50/v2-293f76b25e9afc5d810e86a783eb5c32_qhd.jpg', 'name': '胡小涂', 'url': 'https://www.zhihu.com/people/hu-wen-yan-45', 'gender': -1, 'type': 'zhihu_author', 'id': '96cdd3d64ceb7e25a2dfbb998780f4e4'}, {'avatar_url': 'https://pic4.zhimg.com/50/be38f45b8_qhd.jpg', 'name': 'mofaxuanlv', 'url': 'https://www.zhihu.com/people/zilua', 'gender': 1,'type': 'zhihu_author', 'id': '294f79ab02e666ffcc63d4d56400c03c'}, {'avatar_url': 'https://pic3.zhimg.com/50/f0af76476b5958d6bee1ed0bca8b320b_qhd.jpg', 'name': '孙冰他大姑奶奶', 'url': 'https://www.zhihu.com/people/xiao-pa-11', 'gender': 1, 'type': 'zhihu_author', 'id': 'abdd13cbaa7755f60d80103015d68f14'}, {'avatar_url': 'https://pic4.zhimg.com/50/v2-ee0501398d5895abc672bdb905c8e66e_qhd.jpg', 'name': '故园风雨前', 'url': 'https://www.zhihu.com/people/gu-yuan-feng-yu-qian', 'gender': -1, 'type': 'zhihu_author', 'id': '7a5c80a0c1a7dab3f803915216fb8be4'}, {'avatar_url': 'https://pic1.zhimg.com/50/v2-b3231107c71182f8abcf5c2133823463_qhd.jpg', 'name': '谢青皮', 'url': 'https://www.zhihu.com/people/huang-han-24-67', 'gender': 1, 'type': 'zhihu_author', 'id': 'd9b92dc58183c94b63be0ab98aff5664'}, {'avatar_url': 'https://pic3.zhimg.com/50/7c1443924_qhd.jpg', 'name': '李昭鸿', 'url': 'https://www.zhihu.com/people/li-zhao-hong-14', 'gender': 1, 'type': 'zhihu_author', 'id': 'b56416f32d38f5d9f3916541effaff0a'}, {'avatar_url': 'https://pic1.zhimg.com/50/v2-040853e258ec63581b07bb53d5d2ed5c_qhd.jpg', 'name': 'TimberNord', 'url': 'https://www.zhihu.com/people/timbernord', 'gender': 1, 'type': 'zhihu_author', 'id': '414db84fa848fd8df392c9d8ff36b4f6'}], 'book_version': '180228001', 'corner_text': 'FREE', 'promotion': {'pay_type': 'none', 'is_promotion': False, 'zhihu_bean': 0, 'price': 0, 'origin_price': 0}, 'book_hash': 'd1cdfd044d622afcb5ad1495531064af'},
#  {'is_own': False, 'type': 'ebook', 'description': '终结亲密关系的 12 个困境', 'title': '为什么你的爱情总是不尽人意？', 'url': 'https://www.zhihu.com/pub/book/119567697', 'cover': 'https://pic1.zhimg.com/v2-8d7b81a1b4b286a08177a78a2d796fe6_xld.jpg', 'book_size': 1370274, 'id': 119567697, 'score': 9.0, 'authors': [{'avatar_url': 'https://pic3.zhimg.com/50/v2-a188f1b1ac34ab6feeb167a2594c1de8_qhd.jpg', 'name': '简单心理', 'url': 'https://www.zhihu.com/org/jian-dan-xin-li', 'gender': -1, 'type': 'zhihu_author', 'id': 'e296ed6bc928b9c5055fb210fa79411e'}], 'book_version': '180810004', 'corner_text': '', 'promotion': {'pay_type': 'wallet', 'is_promotion': False, 'zhihu_bean': 799,'price': 799, 'origin_price': 799}, 'book_hash': '51b8a4dc616edfcf9ba6e92ae7f2b751'},
#   {'is_own': False, 'type': 'ebook', 'description': '本书为中国哲学泰斗冯友兰先生的经典著作，乃认识中国哲学的第一入门书。', 'title': '中国哲学简史', 'url': 'https://www.zhihu.com/pub/book/119557727', 'cover': 'https://pic4.zhimg.com/v2-c6813f485334a3d09cb136e1e60d81f3_xld.jpg', 'book_size': 1950536, 'id': 119557727, 'score': 7.8, 'authors': [{'avatar_url': 'https://pic3.zhimg.com/50/v2-171c6620eb0998408c904e81751d9628_qhd.jpg','name': '冯友兰', 'url': '', 'gender': 1, 'type': 'outer_author', 'id': ''}], 'book_version': '180208001', 'corner_text': '', 'promotion': {'pay_type': 'wallet', 'is_promotion': False, 'zhihu_bean': 2299, 'price': 2299, 'origin_price': 2299}, 'book_hash': 'f3e0c7dec7dbe2d644fab3335e55c96c'},
#    {'is_own': False, 'type': 'ebook', 'description': '颠覆你对《一千零一夜》的认知', 'title': '阿拉伯帝国的落日', 'url': 'https://www.zhihu.com/pub/book/119567877', 'cover': 'https://pic4.zhimg.com/v2-70837d1084fcfc285b3cac305390d0f1_xld.jpg', 'book_size': 1853674, 'id': 119567877, 'score': 9.5, 'authors': [{'avatar_url': 'https://pic3.zhimg.com/50/0939d9740600d17b2dbf9fffd569e42b_qhd.jpg', 'name': '男爵兔', 'url': 'https://www.zhihu.com/people/nan-jue-tu', 'gender': -1, 'type': 'zhihu_author', 'id': '3421fa0e4dacfc1296b3e47e50339976'}], 'book_version': '180818002', 'corner_text': '', 'promotion': {'pay_type': 'wallet', 'is_promotion': False, 'zhihu_bean': 599, 'price': 599, 'origin_price': 599}, 'book_hash': '61f9f5e00f34ebaee6947bdf11ff241d'}, 
#    {'is_own': False, 'type': 'ebook', 'description': '不看不知道，一看吓一跳的「神人」探险 ~', 'title': '出发吧！大探险家', 'url': 'https://www.zhihu.com/pub/book/119567052', 'cover': 'https://pic2.zhimg.com/v2-8706d03592209b0c20a2beba0d457b5a_xld.jpg', 'book_size': 1936632, 'id': 119567052, 'score': 9.6, 'authors': [{'avatar_url': 'https://pic2.zhimg.com/50/v2-b429b19a99440e44ed444a56480c5944_qhd.jpg', 'name': '闪米特', 'url': 'https://www.zhihu.com/people/SemitLee', 'gender': 1, 'type': 'zhihu_author','id': 'f926030bec6727bc77fa9f700326fe28'}, {'avatar_url': 'https://pic3.zhimg.com/50/v2-beaabeb81b8b39e8307308b522925db9_qhd.jpg', 'name': '金泰宇', 'url': 'https://www.zhihu.com/people/lostin', 'gender': 1, 'type': 'zhihu_author', 'id': 'b34896a7d1330cd7d6a8be5d1df4072c'}, {'avatar_url': 'https://pic2.zhimg.com/50/v2-ecd9523b298d9b86bc8b25c73ed9ebb3_qhd.jpg', 'name': '极之美', 'url': 'https://www.zhihu.com/people/tripolers', 'gender': 1, 'type': 'zhihu_author', 'id': '1a8f89eede9f250b6d0cb5ef6cdcd225'}, {'avatar_url': 'https://pic4.zhimg.com/50/v2-df3e53a0c2734189d68edea1107350c5_qhd.jpg', 'name': '张经纬', 'url': 'https://www.zhihu.com/people/jw-zhang-62', 'gender': 1, 'type': 'zhihu_author', 'id': 'd405a260a314f094a371ca71d1b6d6d7'}, {'avatar_url': 'https://pic3.zhimg.com/50/v2-0781b2214bf66133379ced59708811c0_qhd.jpg', 'name': '户外探险杂志', 'url': 'https://www.zhihu.com/org/hu-wai-tan-xian-za-zhi', 'gender': -1, 'type': 'zhihu_author', 'id':'c87408d027c25ed16bac8dc00768ac07'}, {'avatar_url': 'https://pic4.zhimg.com/50/v2-a9ba842956f0b565e610b96a658d1e99_qhd.jpg', 'name': '张明', 'url':'https://www.zhihu.com/people/zhang-ming-18-93', 'gender': 1, 'type': 'zhihu_author', 'id': 'db103893062c1bd1b03b97753c5c04e9'}, {'avatar_url': 'https://pic2.zhimg.com/50/v2-6a67cb050387296b04285a558aa7e3d3_qhd.jpg', 'name': '万象历史', 'url': 'https://www.zhihu.com/org/wan-xiang-li-shi', 'gender': -1, 'type': 'zhihu_author', 'id': 'a47f6adcafa4f6367d705856bf9638ed'}, {'avatar_url': 'https://pic2.zhimg.com/50/v2-8e7689e83d03f7735cbd57fb2d81bfc6_qhd.jpg', 'name': '科技每日推送', 'url': 'https://www.zhihu.com/org/ke-ji-mei-ri-tui-song', 'gender': -1, 'type': 'zhihu_author', 'id': '92429137df4eacca1b76089d33ef0e60'}, {'avatar_url': 'https://pic2.zhimg.com/50/v2-3f0eecf91a602babd539f309e5b41b61_qhd.jpg', 'name': '语忆情感研究所', 'url': 'https://www.zhihu.com/org/yu-yi-qing-gan-yan-jiu-suo', 'gender': -1, 'type': 'zhihu_author', 'id': '3407c072565459b198885416dd79aeb3'}], 'book_version': '180712005', 'corner_text': 'FREE', 'promotion': {'pay_type': 'none', 'is_promotion': False, 'zhihu_bean': 0, 'price': 0, 'origin_price': 0}, 'book_hash': '3e50c32ca1f6960106f902489224272f'}]



if __name__ == '__main__':
    main()