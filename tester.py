import asyncio
import aiohttp
from loguru import logger
from fake_headers import Headers
from model import Proxy
from storage import RedisClient
from settings import PROXY_SCORE_MAX, PROXY_SCORE_LEVEL, PROXY_SCORE_STRIDE, TEST_URL, TEST_TIMEOUT


class Tester:

    def __init__(self):
        self.db = RedisClient()
        self.loop = asyncio.get_event_loop()
        self.headers = Headers(headers=True).generate()

    async def test(self, proxy: Proxy):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            logger.info(f'testing {str(proxy)}')
            try:
                async with session.get(TEST_URL, headers=self.headers, proxy=f'http://{str(proxy)}',
                                       timeout=TEST_TIMEOUT, allow_redirects=False):
                    # 没出现异常就算测试通过
                    self.db.add(proxy, PROXY_SCORE_MAX)
            except:
                self.db.decrease(proxy)
                logger.info(f'proxy {str(proxy)} is invalid')

    @logger.catch
    def run(self):
        count = self.db.count()
        logger.info(f'{count} proxies to test')
        # 每次测试一个区间内的所有代理
        for i in range(1, PROXY_SCORE_LEVEL + 1):
            proxies = self.db.batch((i - 1) * PROXY_SCORE_STRIDE + 1, i * PROXY_SCORE_STRIDE)
            if proxies:
                tasks = [self.test(proxy) for proxy in proxies]
                self.loop.run_until_complete(asyncio.wait(tasks))
