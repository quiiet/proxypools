from proxypools.my_redis.redis_func import RedisSave, urls, TIMEOUT, VALID_CODE, BATCH_TEST_SIZE
from aiohttp import ClientProxyConnectionError, ServerDisconnectedError, ClientOSError, ClientHttpProxyError
from asyncio import TimeoutError
import aiohttp
import asyncio
import time

exceptions = (
    ClientProxyConnectionError,
    ConnectionRefusedError,
    TimeoutError,
    ServerDisconnectedError,
    ClientOSError,
    ClientHttpProxyError,
    AssertionError
)

class ValidTester(object):
    def __init__(self):
        self.redis = RedisSave()


    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                print('正在测试：', proxy)
                responses = []#响应码列表
                for i in range(0, len(urls)):
                    url = urls[i].get('url')
                    async with session.get(url, proxy=proxy, timeout=TIMEOUT) as response:
                        if response.status == VALID_CODE:
                            responses.append(1)
                        else:
                            responses.append(0)
                total = 0
                for flag in responses:
                    total += flag
                if total / len(responses) == 1:
                    print('代理可用', proxy)
                    self.redis.max(proxy)
                else:
                    print('请求响应码不合法', proxy)
                    self.redis.decrease(proxy)

            except exceptions:
                self.redis.decrease(proxy)
                print('请求响应码不合法', proxy)


    def run(self):
        print('测试器开始执行')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i:i + BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)

        except  exceptions as e:
            print('测试器错误', e.args)
                



    

    
