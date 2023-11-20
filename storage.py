from random import choice
from typing import List
import redis
from loguru import logger
from model import Proxy
from settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB, REDIS_KEY, \
        PROXY_SCORE_MIN, PROXY_SCORE_MAX, PROXY_SCORE_INIT, PROXY_NUMBER_MAX


class RedisClient:

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB):
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=db, decode_responses=True)

    def add(self, proxy: Proxy, score=PROXY_SCORE_INIT) -> int:
        if score == PROXY_SCORE_INIT:
            if self.exists(proxy):
                return 0
        return self.db.zadd(REDIS_KEY, {str(proxy): score})

    def random(self) -> Proxy:
        proxies = self.db.zrangebyscore(REDIS_KEY, PROXY_SCORE_MAX, PROXY_SCORE_MAX)
        if len(proxies):
            proxy = choice(proxies)
            host, port = proxy.split(':')
            return Proxy(host, int(port))
        proxies = self.db.zrevrange(REDIS_KEY, PROXY_SCORE_MIN, PROXY_SCORE_MAX)
        if len(proxies):
            proxy = choice(proxies)
            host, port = proxy.split(':')
            return Proxy(host, int(port))
        raise Exception('no data in proxypool')

    def decrease(self, proxy: Proxy) -> None:
        self.db.zincrby(REDIS_KEY, -5, str(proxy))
        score = self.db.zscore(REDIS_KEY, str(proxy))
        logger.info(f'{str(proxy)} score decrease 5, current score {score}')
        if score <= PROXY_SCORE_MIN:
            logger.info(f'{str(proxy)} current score {score}, remove it')
            self.db.zrem(REDIS_KEY, str(proxy))

    def count(self) -> int:
        return self.db.zcard(REDIS_KEY)

    def exists(self, proxy: Proxy) -> bool:
        return self.db.zscore(REDIS_KEY, str(proxy)) is not None

    def batch(self, start: int, end: int) -> List[Proxy]:
        proxies = self.db.zrangebyscore(REDIS_KEY, start, end)
        ret = []
        for proxy in proxies:
            host, port = proxy.split(':')
            ret.append(Proxy(host=host, port=int(port)))
        return ret

    def is_full(self) -> bool:
        return self.count() >= PROXY_NUMBER_MAX
