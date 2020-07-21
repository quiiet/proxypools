import sys
import os
sys.path.append(os.getcwd() + '\\proxypools\\my_redis\\redis_func.py')
from proxypools.my_redis.redis_func import RedisSave, THRESHOLD

class Getter(object):

    def __init__(self):
        self.redis = RedisSave()


    def is_over_threshold(self):
        if self.redis.count() >= THRESHOLD:
            return True
        else:
            return False


    def run(self, list):
        i = 0
        print('正在存入redis')
        if not self.is_over_threshold():
            for proxy in list:
                print('正在存入', proxy)
                i += 1
                self.redis.add(proxy)
