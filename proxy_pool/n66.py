#获取模块
#从ip66.cn爬取代理

import requests
from lxml import html
from proxy_pool.db import RedisClient
import time


my_head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.132 Safari/537.36'}

#延迟&返回要获取的html
def get_html(url,decode):
    time.sleep(2)
    return requests.get(url, headers=my_head).content.decode(decode)

#
def crawl_66proxy(pagenumber):
    url = "http://www.66ip.cn/{}.html"
    client = RedisClient()                                      #设置数据库为redis
    for i in range(1, pagenumber+1):                            #循环获取要访问的网址
        new_url = url.format(i)
        htmlcont = get_html(new_url,'GBK')
        selector = html.fromstring(htmlcont)                    #用selector获取网页源码
        iplist = selector.xpath("//tr/td[1]/text()")            #正则表达式获取其中的ip
        portlist = selector.xpath("//tr/td[2]/text()")


        for item in zip(iplist[3:-1], portlist[1:-1]):          #合并ip和port
            client.add(":".join(item))


if __name__=='__main__':
    crawl_66proxy(3)