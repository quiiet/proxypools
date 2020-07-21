import redis
import json
from random import choice
from proxypools.utils import get_config
import os
import sys
path = '\\proxypools\\my_redis\\filter_settings.json'

HOST = get_config(path, 'HOST')
PASSWORD = get_config(path, 'PASSWORD')
PORT = get_config(path, 'PORT')
DB = get_config(path, 'DB')
KEY = get_config(path, 'KEY')
INITIAL = get_config(path, 'INITIAL')
MAX = get_config(path, 'MAX')
MIN = get_config(path, 'MIN')
THRESHOLD = get_config(path, 'THRESHOLD')
urls = get_config(path, 'test_urls')
TIMEOUT = get_config(path, 'TIMEOUT')
VALID_CODE = get_config(path, 'VALID_CODE')
BATCH_TEST_SIZE = get_config(path, 'BATCH_TEST_SIZE')

class RedisSave(object):
    def __init__(self, host=HOST, port=PORT, password=PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=None, db=DB ,decode_responses=True)


    def add(self, proxy, score=INITIAL):
        if not self.db.zscore(KEY, proxy):
            return self.db.zadd(KEY, score, proxy)


    def random(self):
        result = self.db.zrangebyscore(KEY, MAX, MAX)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrangebyscore(KEY, MIN, MAX)
            if len(result):
                return choice(result)
            else:
                print('no proxy in proxypools')


    def decrease(self, proxy):
        score = self.db.zscore(KEY, proxy)
        if score and score > MIN:
            print('代理', proxy, '当前分数', score, '减一')
            return self.db.zincrby(KEY, proxy, -1)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(KEY, proxy)



    def exists(self, proxy):
        return not self.db.zscore(KEY, proxy) == None



    def max(self, proxy):
        print('代理', proxy, '可用，设置为', MAX)
        return self.db.zadd(KEY, MAX, proxy)


    def count(self):
        return self.db.zcard(KEY)



    def all(self):
        return self.db.zrangebyscore(KEY, MIN, MAX)
