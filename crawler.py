from loguru import logger
from storage import RedisClient
from spiders.public.kuaidaili import KuaidailiSpider


class Crawler:

    def __init__(self):
        self.db = RedisClient()
        self.crawlers = [
            KuaidailiSpider(),
        ]

    def run(self):
        if self.db.is_full():
            return
        for crawler in self.crawlers:
            logger.info(f'crawler {crawler} to get proxy')
            for proxy in crawler.crawl():
                self.db.add(proxy)
