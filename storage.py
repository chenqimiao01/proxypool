from random import choice
from typing import List
import redis
from loguru import logger
from model import Proxy
from settings import REDIS_URL, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB, REDIS_KEY, \
        PROXY_SCORE_MIN, PROXY_SCORE_MAX, PROXY_SCORE_INIT, PROXY_NUMBER_MAX

class RedisClient:

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB, 
            url=REDIS_URL):
        if url:
            self.db = redis.StrictRedis.from_url(url, decode_responses=True)
        else:
            self.db = redis.StrictRedis(host=host, port=port, password=password, db=db, decode_responses=True)

    def zadd(self, proxy: Proxy, score=PROXY_SCORE_INIT) -> int:
        if score == PROXY_SCORE_INIT:
            if self.zscore(proxy):
                return 0
        logger.info(f'{str(proxy)} is valid, set to {score}')
        return self.db.zadd(REDIS_KEY, {str(proxy): score})

    def zrandom(self) -> Proxy:
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

    def zdecrby(self, proxy: Proxy) -> None:
        self.db.zincrby(REDIS_KEY, -1, str(proxy))
        score = self.db.zscore(REDIS_KEY, str(proxy))
        logger.info(f'{str(proxy)} score decrease 1, current score {score}')
        if score <= PROXY_SCORE_MIN:
            logger.info(f'{str(proxy)} current score {score}, remove it')
            self.db.zrem(REDIS_KEY, str(proxy))

    def zcard(self) -> int:
        return self.db.zcard(REDIS_KEY)

    def zscore(self, proxy: Proxy) -> bool:
        return self.db.zscore(REDIS_KEY, str(proxy)) != None

    def zrangebyscore(self, start: int, end: int) -> List[Proxy]:
        proxies = self.db.zrangebyscore(REDIS_KEY, start, end)
        ret = []
        for proxy in proxies:
            host, port = proxy.split(':')
            ret.append(Proxy(host=host, port=int(port)))
        return ret

    def zfull(self) -> bool:
        return self.zcard() >= PROXY_NUMBER_MAX
