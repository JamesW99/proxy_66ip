from time import sleep
from bs4 import BeautifulSoup
import requests
import re
from pymongo import MongoClient

client = MongoClient()

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36' }

url = "https://maoyan.com/board/4?"

database = client['movies']
collection = database['topmovie+score']

for i in range(0, 10):                                               # 循环获取网址
    offset = i * 10
    new_url = url + "offset=" + str(offset)
    print(new_url)
    sleep(5)

    cont = requests.get(new_url, headers=headers).content.decode()

    soup = BeautifulSoup(cont, 'lxml')
    # print(cont)
    results = soup.find_all(class_='board-item-content')               #class是关键词
    # print(len(results))
    all_record = []

    for items in results:                                            #获取关键信息
        record = {}

        item = items.find(class_='movie-item-info')
        item2 = items.find(class_='movie-item-number score-num')

        record['name'] = item.find(class_="name").text.strip()
        record['stars'] = item.find(class_="star").text.strip()
        record['time'] = re.findall('上映时间：([-0-9]*)', item.find(class_="releasetime").text, re.S)[0]

        front = item2.find(class_="integer")
        rear = item2.find(class_="fraction")
        record['score'] = int(front.text.replace('.', ' ')) + int(rear.text) * 0.1           #把front和rear转化成int，相加

        all_record.append(record)

    print(all_record)
    collection.insert_many(all_record)