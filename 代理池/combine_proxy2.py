from multiprocessing import Process
from craw_file_stu import crawl_66proxy
from test_proxy_stu2 import test_proxy_in_redis
from web_proxy_stu import app
from time import sleep

PAGES_NUMBER = 3

CRAWL_MODE = True
TEST_MODE = True
API_MODE = True

CRAWL_CYCLE = 20
TEST_CYCLE = 20



def schedule_crawl(CYCLE=CRAWL_CYCLE):
    while True:
        print("爬取数据开始")
        crawl_66proxy(PAGES_NUMBER)
        sleep(CYCLE)




def schedule_test(CYCLE=TEST_CYCLE):
    while True:
        print("test数据开始")
        test_proxy_in_redis()
        sleep(CYCLE)



def schedule_server():
    app.run("127.0.0.1", 5000)



def schedue_work():
    if CRAWL_MODE:
        crawler_process = Process(target=schedule_crawl)
        crawler_process.start()

    if TEST_MODE:
        test_process = Process(target=schedule_test)
        test_process.start()

    if API_MODE:
        app_process = Process(target=schedule_server)
        app_process.run()



if __name__=='__main__':
    schedue_work()