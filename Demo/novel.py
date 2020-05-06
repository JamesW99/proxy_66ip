import re
import requests
from lxml import html

url="https://www.kanunu8.com/book3/6879/"
cont = requests.get(url).content.decode("GBK")

new_urls = re.findall('href="([^<]*?)">第',cont, re.S)

chapter = 1
for item in new_urls:
    nurl = url + item
    ncont = requests.get(nurl).content.decode("GBK")    #获取gbk源码
    selector = html.fromstring(ncont)
    paragraph = selector.xpath("//p/text()")
    with open(r"/Users/james/Downloads/interchange/" + str(chapter) + '.txt','a')as log:
        log.writelines(paragraph)
    chapter += 1