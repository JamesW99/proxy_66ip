from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

client = MongoClient()

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36' }

url = "https://maoyan.com/board/4?"

database =client['movies']
collection = database['score']

for i in range(0,10):                                               #循环获取网址
    offset = i*10
    new_url= url + "offset=" + str(offset)
    cont=requests.get(new_url,headers=headers).content.decode()
    soup = BeautifulSoup(cont,'lxml')
    results = soup.find_all(class_="movie-item-number score-num")

    for item in results:                                            #获取分

        front = item.find(class_="integer")
        rear  = item.find(class_="fraction")
        score= int(front.text.replace('.',' ')) + int(rear.text) *0.1           #把front和rear转化成int，相加