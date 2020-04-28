import pymysql
import requests
from lxml import etree


def get_movies(page):
    url = "https://www.xinpianchang.com/channel/index/type-/sort-like/duration_type-0/resolution_type-/page-%s" % page
    # 获取url中的内容
    response = requests.get(url)

    html_content = response.text

    # 使用xpath进行内容解析
    html = etree.HTML(html_content)
    # 根据规则提取内容
    movies = html.xpath("/html/body/div[8]/div[2]/ul/li")

    # 存入数据库
    dbParmas = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '123',
        'db': 'film',
        'port': 3306,
        'charset': 'utf8'
    }
    conn = pymysql.Connect(**dbParmas)  # 任意关键字参数

    # 获取游标
    cursor = conn.cursor()

    for movie in movies:
        title = movie.xpath("./div/div[1]/a/p/text()")[0]
        cover_image = movie.xpath("./a/img/@_src")[0]
        durations = movie.xpath("./a/span/text()")
        if durations:
            duration = durations[0]
        else:
            duration = '无信息'
        publish_time = movie.xpath("./a/div[2]/p/text()")[0]
        cate = movie.xpath("./div/div[1]/div[1]/span[1]/text()")[0]
        play_num = movie.xpath("./div/div[1]/div[2]/span[1]/text()")[0]
        like_num = movie.xpath("./div/div[1]/div[2]/span[2]/text()")[0]
        descriptions = movie.xpath("./a/div[2]/div/text()")
        if descriptions:
            description = descriptions[0]
        else:
            description = "描述"

        print(title, cover_image, duration, description, publish_time, cate, play_num, like_num)

        # 执行sql  只是添加到执行队列中
        # cursor.execute('INSERT INTO app_movie(cover_image, duration, description, publish_time, title, cate, play_num, like_num) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s");'
        #                % (cover_image, duration, description, publish_time, title, cate, play_num, like_num))
        # # # 提交
        # conn.commit()


if __name__ == '__main__':
    for i in range(2, 10):
        get_movies(i)
