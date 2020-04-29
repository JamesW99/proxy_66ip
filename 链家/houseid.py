'''✅
获取houseid
传入页数默认10&睡眠时间默认60
可调用houseid
'''


import re
import requests
import time


my_head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.132 Safari/537.36'}

#延迟&返回要获取的html
def get_html(url,decode):
    time.sleep(2)
    return requests.get(url, headers=my_head).content.decode(decode)


def get_url(page=10,shui=60):
    houseid = []
    url = "http://bj.lianjia.com/ershoufang/pg"
    for i in range(1, page + 1):
        time.sleep(shui)
        offset = i
        new_url = url + str(offset)
        print(new_url)

        # 获取网页源码
        page =  get_html(new_url,'UTF-8')
        #print(page)

        # 获取id
        dl = re.findall('data-houseid="(.*?)">', page, re.S)
        houseid.extend(dl)
    print(houseid)
    return houseid

if __name__=='__main__':
    get_url(1,1)