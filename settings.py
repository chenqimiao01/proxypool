import os
from loguru import logger

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_DB = 0
REDIS_KEY = 'proxies'

PROXY_SCORE_MAX = 100
PROXY_SCORE_INIT = 10
PROXY_SCORE_MIN = 0

PROXY_NUMBER_MAX = 50000
PROXY_NUMBER_MIN = 0

TEST_URL = 'http://www.baidu.com'
TEST_TIMEOUT = 10
PROXY_SCORE_LEVEL = 25
PROXY_SCORE_STRIDE = 4

# 间隔 20s 测试数据库中的代理是否可用
TEST_CYCLE = 20
# 间隔半天爬取一次
GET_CYCLE = 43200
GET_TIMEOUT = 10


API_HOST = '0.0.0.0'
API_PORT = 5566
API_THREADED = True


LOG_DIR = os.path.join(ROOT_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
logger.add(os.path.join(LOG_DIR, 'runtime.log'), level='INFO', rotation='500MB', retention='1 week')
logger.add(os.path.join(LOG_DIR, 'error.log'), level='ERROR', rotation='500MB')
