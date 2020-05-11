#存储模块
#把n66.py爬取的代理储存到redis数据库中

import redis
from random import choice

MAX_SCORE = 100000
MIN_SCORE = 0
INITIAL_SCORE = 3
REDIS_HOST = 'localhost'

REDIS_PORT = 6379
REDIS_PASSWORD = None

REDIS_KEY = 'proxies'


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化redis数据库的连接
        :param host: redis所在ip
        :param port: redis端口
        :param password: redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理到redis 设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """

        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy:score})

    def random(self):
        """
        随机获取有效代理， 首先尝试获取分数最高代理， 如果没有分数最高代理，按照排名获取。否则异常
        :return: 代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE)
            if len(result):
                return result[0]
            else:
                print("找不到可用代理")
                raise Exception

    def decrease(self, proxy):
        """
        代理数值减分，如果小于最小值，则代理删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减少1')
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def da100(self,proxy):
        score = self.db.zscore(REDIS_KEY, proxy)
        print('代理', proxy, '不可用，但之前可用过，设置为99')
        return self.db.zadd(REDIS_KEY, {proxy: 99})



    def exist(self, proxy):
        """
        判断该代理是否存在
        :param proxy:代理
        :return:是否存在
        """
        return self.db.zscore(REDIS_KEY, proxy) is not None

    def max(self, proxy):
        """
        将代理设置为100分
        :param proxy: 代理
        :return:设置结束
        """
        print('代理', proxy, '可用，设置为100')
        return self.db.zadd(REDIS_KEY, {proxy:100})

    def over_max(self, proxy):
        """
        将代理设置为100分
        :param proxy: 代理
        :return:设置结束
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        print('代理', proxy, '不是第一次可用，分数', score+1)
        return self.db.zincrby(REDIS_KEY, 1, proxy)

    def count(self):
        """
        获取代理的数量
        :return:
        """

        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return:
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)