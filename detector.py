import asyncio
import aiohttp
from loguru import logger
from model import Proxy
from storage import RedisClient
from settings import PROXY_SCORE_MAX, PROXY_SCORE_LEVEL, PROXY_SCORE_STRIDE, TEST_URL, TEST_TIMEOUT


Exceptions = (
    asyncio.TimeoutError, 
    aiohttp.ClientProxyConnectionError,
    ConnectionRefusedError,
    aiohttp.ServerDisconnectedError,
    aiohttp.ClientOSError,
    AssertionError,
    aiohttp.ClientHttpProxyError
)

class Detector:

    def __init__(self):
        self.redis = RedisClient()
        self.loop = asyncio.get_event_loop()

    async def detect(self, proxy: Proxy):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            logger.info(f'testing {str(proxy)}')
            try:
                async with session.get(TEST_URL, proxy=f'http://{str(proxy)}', timeout=TEST_TIMEOUT, 
                        allow_redirects=False) as response:
                    # 没出现异常就算测试通过
                    self.redis.zadd(proxy, PROXY_SCORE_MAX)
            except Exceptions as e:
                self.redis.zdecrby(proxy)
                logger.info(f'proxy {str(proxy)} is invalid, decrease score')

    @logger.catch
    def run(self):
        logger.info('starting detect proxy...')
        count = self.redis.zcard()
        logger.info(f'{count} proxies to test')
        # 每次测试一个区间内的所有代理
        for i in range(1, PROXY_SCORE_LEVEL + 1):
            proxies = self.redis.zrangebyscore((i - 1) * PROXY_SCORE_STRIDE + 1, i * PROXY_SCORE_STRIDE)
            if proxies:
                tasks = [self.detect(proxy) for proxy in proxies]
                self.loop.run_until_complete(asyncio.wait(tasks))
