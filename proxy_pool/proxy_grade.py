import requests
from proxy_pool.db import RedisClient
import redis

REDIS_KEY = 'proxies'

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def is_bad_proxy(proxy, default_server="http://httpbin.org/get"):

    score = r.zscore(REDIS_KEY, proxy)

    proxies = {
        'http': 'http://' + proxy,
        'https': 'http://' + proxy,
    }

    redis = RedisClient()

    try:                                                    #异常匹配
        res = requests.get(default_server, proxies=proxies, timeout=5)
        if res.status_code == 200:
            print("{} 代理可用".format(proxy))
            if score < 100:
                redis.max(proxy)                    #第一次可用，设置为100
            else:
                redis.over_max(proxy)               #多次可用，设置为score+1
        else:                                               #返回404之类的
            print("{}代理不可用".format(proxy))
            score = r.zscore(REDIS_KEY, proxy)
            if score>99:
                redis.da100(proxy)                  #不可用，之前可用——设置为99
    except requests.exceptions.RequestException as e:       #无响应
        print(e)
        redis.decrease(proxy)


def test_proxy_in_redis():                                  #测试所有代理
    redis = RedisClient()
    proxy_all = redis.all()
    #print(proxy_all)

    for item in proxy_all:
        is_bad_proxy(item)


if __name__ == '__main__':                                  #只有从当前页面run才会运行本行
    test_proxy_in_redis()