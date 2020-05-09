'''
调用houseid.py，获取page*30个houseid
把houseid组成url，通过xpath获取房屋detail
存入数据库
'''
import re
import requests
from lxml import html
import time
from lianjia.houseid import get_url
from pymongo import MongoClient


url = 'https://bj.lianjia.com/ershoufang/'
my_head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.132 Safari/537.36'}

client = MongoClient()
database = client['链家']
collection = database['北京二手房']

shui = 2
houseid = get_url(100,shui)           # 调用house id，返回所有要获取的id


# 这个函数只能调用一次！！！
# 所以他要返回一整页代码
# 延迟返回要获取的html     #改成返回源码
def get_sc(i):
    time.sleep(shui)
    full_url= url+ houseid[i]+'.html'
    print(full_url)
    sc = requests.get(full_url, headers=my_head).content.decode('UTF-8')      # 调用get_html 获取网页源码
    #print (sc)
    return sc


# 调用get_html获取源码 输入要访问的页码（z）
# 传入xpath，
# 将url头+houseid 合并为new url & 判断是否为空。空返回none，else返回的内容
def check_none(xp, selector):
    neirong = None
    if selector.xpath(xp):
        #要在结尾加[0]，把list转化成str，不然数据库中显示不出来
        neirong = selector.xpath(xp)[0]
    #print(neirong)
    return neirong



# 储存变量名和要获取的内容。循环 传入xpath 调用checknone来获取内容。存入字典，存入数据库
def get_detail():
    all_record = []
    for z in range(len(houseid)):

        sc = get_sc(z)
        selector = html.fromstring(sc)          #得到第z页的源码了
        print(selector)

        title = check_none('//title/text()', selector)
        price = check_none('//div[5]/div[2]/div[3]/span[1]/text()', selector)
        danwei = check_none('//div[5]/div[2]/div[3]/span[2]/span/text()', selector)
        sumprice = price+danwei
        name = check_none('//div[5]/div[2]/div[5]/div[1]/a[1]/text()', selector)
        district = check_none('//div[5]/div[2]/div[5]/div[2]/span[2]/a[1]/text()', selector)
        location = check_none('//div[5]/div[2]/div[5]/div[2]/span[2]/a[2]/text()', selector)
        gtime = check_none('//div/div/div[2]/div[2]/ul/li[1]/span[2]/text()', selector)
        huxing = check_none('//div/div/div[1]/div[2]/ul/li[1]/text()', selector)
        mianji = check_none('//div/div/div[1]/div[2]/ul/li[3]/text()', selector)
        tihubi = check_none('//div/div/div[1]/div[2]/ul/li[10]/text()', selector)
        floor = check_none('//div/div/div[1]/div[2]/ul/li[2]/text()', selector)
        yongtu = check_none('//div/div/div[2]/div[2]/ul/li[4]/span[2]/text()', selector)
        redu = check_none('//*[@id="favCount"]/text()', selector)
        chaoxiang = check_none('//div/div/div[1]/div[2]/ul/li[7]/text()', selector)
        nuan = check_none('//div/div/div[1]/div[2]/ul/li[11]/text()', selector)
        dianti = check_none('//div/div/div[1]/div[2]/ul/li[12]/text()', selector)
        id = check_none('//div[5]/div[2]/div[5]/div[4]/span[2]/text()', selector)
        jianjie2 = check_none('//div[7]/div[1]/div[2]/div/div[2]/div[2]/text()', selector)
        jianjie = None
        danjia = None
        if jianjie2:
            jianjie1 = "".join(jianjie2)  # 转化为str
            jianjie = jianjie1.strip()  # 去掉两边空格和换行符
        if mianji:
            mianjis = re.findall(r"\d+\.?\d*", mianji)  #去掉单位的价格，类型list
            a = "".join(mianjis)                        #list转换为str
            b = "".join(price)
            danjia = float(b) / float(a)                #转换float 相除


        dic = {
            '标题' : title,
            '总价' : sumprice,
            '小区': name,
            '区' : district,
            '商圈' : location,
            '挂牌时间' : gtime,
            '户型' : huxing,
            '面积' : mianji,
            '梯户比例' : tihubi,
            '楼层' : floor,
            '用途' : yongtu,
            '关注人数' : redu,
            '朝向' : chaoxiang,
            '供暖方式' : nuan,
            '电梯' : dianti,
            '单价' : danjia,
            '介绍' : jianjie,
            'ID' : id

        }
        print(dic)
        all_record.append(dic)
    collection.insert_many(all_record)





# 开始！
if __name__=='__main__':
    get_detail()
