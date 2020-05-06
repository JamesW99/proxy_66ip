import requests
from proxy_pool.db import RedisClient


def is_bad_proxy(proxy, default_server="http://httpbin.org/get"):

    proxies = {
        'http': 'http://' + proxy,
        'https': 'http://' + proxy,
    }

    redis = RedisClient()

    try:                                                    #异常匹配
        res = requests.get(default_server, proxies=proxies, timeout=5)
        if res.status_code == 200:
            print("{} 代理可用".format(proxy))
            redis.max(proxy)
        else:                                               #返回404之类的
            print("{}代理不可用".format(proxy))
            redis.decrease(proxy)
    except requests.exceptions.RequestException as e:       #无响应
        print(e)
        redis.decrease(proxy)


def test_proxy_in_redis():                                  #测试所有代理
    redis = RedisClient()
    proxy_all = redis.all()

    for item in proxy_all:
        is_bad_proxy(item)


if __name__ == '__main__':                                  #只有从当前页面run才会运行本行
    test_proxy_in_redis()