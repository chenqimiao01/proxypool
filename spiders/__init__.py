import time
import requests
from loguru import logger
from fake_headers import Headers
from retrying import RetryError, retry
from settings import GET_TIMEOUT


class Spider:

    urls = []
    encoding = 'utf-8'

    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
    def fetch(self, url):
        try:
            headers = Headers(headers=True).generate()
            r = requests.get(url, headers=headers, timeout=GET_TIMEOUT)
            if r.status_code == 200:
                r.encoding = self.encoding
                return r.text
            return None
        except (requests.ConnectionError, requests.ReadTimeout):
            return None

    def process(self, html, url):
        for proxy in self.parse(html):
            logger.info(f'fetching proxy {str(proxy)} from {url}')
            yield proxy

    def parse(self, html):
        raise NotImplementedError

    def crawl(self):
        try:
            for url in self.urls:
                logger.info(f'fetching {url}')
                html = self.fetch(url)
                if not html:
                    continue
                time.sleep(0.5)
                yield from self.process(html, url)
        except RetryError:
            logger.error(f'crawler {self} crawled proxy failed, please check if target url is valid or network issue')
