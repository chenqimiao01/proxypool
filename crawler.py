from loguru import logger
from storage import RedisClient
from spiders.public.kuaidaili import KuaidailiSpider


class Crawler:

    def __init__(self):
        self.redis = RedisClient()
        self.crawlers = [
            KuaidailiSpider(),
        ]

    def run(self):
        if self.redis.zfull():
            return
        for crawler in self.crawlers:
            logger.info(f'crawler {crawler} to get proxy')
            for proxy in crawler.crawl():
                self.redis.zadd(proxy)
