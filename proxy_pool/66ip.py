import time
from lxml import html
import requests
from pymongo import MongoClient

client = MongoClient()

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.132 Safari/537.36'}

url = "http://www.66ip.cn/"

database = client['代理']
collection = database['66ip.cn']

page = 2
all_record = []
for i in range(2, 10):  # 循环获取网址
#for i in range(3, 4):  # 循环获取网址
    time.sleep(2)
    offset = i
    new_url = url + str(offset) + ".html"
    print(new_url)


#获取网页源码
    page = requests.get(new_url).content.decode('GBK')
    #print(page)

    selector = html.fromstring(page)


# 正则表达式 从tr[2]/td[1] 取到tr[13]/td[2] 获取ip&port
    for t in range(2,14):
        a = "//tr[" + str(t) + "]/td[1]/text()"
        b = "//tr[" + str(t) + "]/td[2]/text()"
        ip = selector.xpath(a)
        port = selector.xpath(b)
        quan = str(ip) +':'+str(port)       #合并字符串
        s = quan.replace("'","")            #去掉符号
        s = s.replace("[", "")
        s = s.replace("]", "")
        # print(ip)
        # print(s)

        # 放入数据库 代码来film list.py
        record = {}
        record['s'] = s.strip()
        all_record.append(record)

    print(all_record)
    collection.insert_many(all_record)




'''
    with open(r"/Users/james/Downloads/interchange/aaa.txt" ,"w")as log:
        log.write(new_url)
    chapter += 1
'''


# 放入数据库