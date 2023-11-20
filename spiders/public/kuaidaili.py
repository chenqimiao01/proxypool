from lxml import etree
from loguru import logger
from model import Proxy
from spiders import Spider
from utils import is_ipv4, is_port


BASE_URL = 'https://www.kuaidaili.com/free/{type}/{page}'
MAX_PAGE = 3


class KuaidailiSpider(Spider):

    urls = [BASE_URL.format(type=type, page=page) for type in ('intr', 'inha') for page in range(1, MAX_PAGE + 1)]

    def parse(self, html):
        doc = etree.HTML(html)
        for item in doc.xpath('//*[@id="list"]//table/tbody/tr'):
            host = item.xpath('./td[@data-title="IP"]/text()')[0]
            port = item.xpath('./td[@data-title="PORT"]/text()')[0]
            if is_ipv4(host) and is_port(port):
                yield Proxy(host=host, port=int(port))
            else:
                logger.info(f'invalid proxy {host}:{port}, throw it')
