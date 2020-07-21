import sys
import os
sys.path.append(os.getcwd()+'\\crawler_ip\\pulic')
sys.path.append(os.getcwd()+'\\my_redis')
sys.path.append(os.getcwd()+'\\server')
path = '\\schedule_settings.json'
from proxypools.my_redis.redis_func import RedisSave
from proxypools.crawler_ip.public.xiaohuan import Crawl_XiaoHuan
from proxypools.crawler_ip.public.ip66 import Crawl_ip66
from proxypools.getter.Getter import Getter
from proxypools.tester.Tester import ValidTester
from proxypools.server.api import app
from multiprocessing import Process
from proxypools.utils import get_config
import time

TEST_COUNT = get_config(path, 'TEST_COUNT')
TESTER_CYCLE = get_config(path, 'TESTER_CYCLE')
GETTER_CYCLE = get_config(path, 'GETTER_CYCLE')
TESTER_ENABLE = get_config(path, 'TESTER_ENABLE')
GETTER_ENABLE = get_config(path, 'GETTER_ENABLE')
API_ENABLE = get_config(path, 'API_ENABLE')

class Scheduler(object):

    def __init__(self):
        pass


    def schedule_getter(self):
        #获取模块
        list = []
        Crawl_ip66().run(list)
        Crawl_XiaoHuan().run(list)
        Getter().run(list)
        
    def schedule_tester(self):
        for i in range(TEST_COUNT):
            ValidTester().run()

    
    def schedule_api(self):
        app.run('127.0.0.1', 5555)


    def run(self):
        print('代理池开始运行\n')
        
        time.sleep(2)
        if TESTER_ENABLE:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()


        if GETTER_ENABLE:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLE:
            api_process = Process(target=self.schedule_api)
            api_process.start()


if __name__ == "__main__":
    start = Scheduler()
    start.run()
