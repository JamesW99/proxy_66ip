'''
调用houseid.py，获取page*30个houseid✅
把houseid组成url，通过xpath获取房屋detail✅
存入数据库

'''



import requests
from lxml import html
import time
from 链家.houseid import get_url



my_head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.132 Safari/537.36'}

#延迟&返回要获取的html
def get_html(url,decode):
    time.sleep(60)
    return requests.get(url, headers=my_head).content.decode(decode)

url = 'https://bj.lianjia.com/ershoufang/'
def get_detail(page,shui):
    houseid = get_url(page,shui)
    for i in houseid:                            #循环获取要访问的网址
        new_url = url+format(i)+'.html'
        #print(new_url)

        code = get_html(new_url,'UTF-8')                        #调用get_html 获取网页源码
        selector = html.fromstring(code)

        title = selector.xpath('//title/text()')
        price = selector.xpath('//div[5]/div[2]/div[3]/span[1]/text()')
        danwei = selector.xpath('//div[5]/div[2]/div[3]/span[2]/span/text()')
        sumprice = price+danwei
        gtime = selector.xpath('//div/div/div[2]/div[2]/ul/li[1]/span[2]/text()')
        huxing = selector.xpath('//div/div/div[1]/div[2]/ul/li[1]/text()')
        mianji = selector.xpath('//div/div/div[1]/div[2]/ul/li[3]/text()')
        tihubi = selector.xpath('//div/div/div[1]/div[2]/ul/li[10]/text()')

        dic = {
            'title' : title,
            'price' : sumprice,
            '挂牌时间' : gtime,
            '户型' : huxing,
            '面积' : mianji,
            '梯户比例' :tihubi

        }
        print(dic)



if __name__=='__main__':
    get_detail(1,1)