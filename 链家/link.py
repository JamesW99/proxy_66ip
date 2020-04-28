#旧的，作废


import time
from lxml import html
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.132 Safari/537.36'}


client = MongoClient()
database = client['链家']
collection = database['link']



# 获取要爬的url
page = 1
all_record = []
url = "http://bj.lianjia.com/ershoufang/pg"
for i in range(1, page+1):
    time.sleep(1)
    offset = i
    new_url = url + str(offset) + "co32/"
    print(new_url)

#获取网页源码✅
    page = requests.get(new_url).content.decode('UTF-8')
    #print(page)

#获取id
#真的取不出来data-houesid，数字匹配凑活一下

    pattern = re.compile(r'\d+')  # 查找数字
    num = re.findall(r'\d+', page)# 所有数字

    dl = re.findall(r'101107\d{6}', page, re.S)
    quchong = list(set(dl))

    print(len(quchong))








