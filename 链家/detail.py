'''
调用houseid.py，获取page*30个houseid✅
把houseid组成url，通过xpath获取房屋detail✅
存入数据库

'''



import requests
from lxml import html
import time
from 链家.houseid import get_url
from pymongo import MongoClient



my_head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.132 Safari/537.36'}

client = MongoClient()
database = client['链家']
collection = database['北京二手房']


#延迟&返回要获取的html
def get_html(url,decode):
    time.sleep(10)
    return requests.get(url, headers=my_head).content.decode(decode)

url = 'https://bj.lianjia.com/ershoufang/'
def get_detail(page,shui):
    houseid = get_url(page,shui)
    all_record = []
    for i in houseid:                            #循环获取要访问的网址
        new_url = url+format(i)+'.html'
        #print(new_url)

        code = get_html(new_url,'UTF-8')                        #调用get_html 获取网页源码
        selector = html.fromstring(code)

        #要在结尾加[0]，把list转化成str，不然数据库中显示不出来
        title = selector.xpath('//title/text()')[0]
        price = selector.xpath('//div[5]/div[2]/div[3]/span[1]/text()')
        danwei = selector.xpath('//div[5]/div[2]/div[3]/span[2]/span/text()')
        sumprice = price[0]+danwei[0]
        gtime = selector.xpath('//div/div/div[2]/div[2]/ul/li[1]/span[2]/text()')[0]
        huxing = selector.xpath('//div/div/div[1]/div[2]/ul/li[1]/text()')[0]
        mianji = selector.xpath('//div/div/div[1]/div[2]/ul/li[3]/text()')[0]
        tihubi = selector.xpath('//div/div/div[1]/div[2]/ul/li[10]/text()')[0]



        dic = {
            'title' : title,
            'price' : sumprice,
            '挂牌时间' : gtime,
            '户型' : huxing,
            '面积' : mianji,
            '梯户比例' :tihubi
        }
        print(dic)
        all_record.append(dic)
    collection.insert_many(all_record)



if __name__=='__main__':
    get_detail(1,1)