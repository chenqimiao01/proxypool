import time
import multiprocessing
from loguru import logger
from crawler import Crawler
from detector import Detector
from settings import GET_CYCLE, TEST_CYCLE


# 子进程句柄
c_process, d_process = None, None


class Scheduler:

    def crawler(self, cycle=GET_CYCLE):
        c = Crawler()
        loop = 0
        while True:
            logger.info(f'getter loop {loop} start')
            c.run()
            loop += 1
            time.sleep(cycle)

    def detector(self, cycle=TEST_CYCLE):
        d = Detector()
        loop = 0
        while True:
            logger.info(f'tester loop {loop} start...')
            d.run()
            loop += 1
            time.sleep(cycle)

    def run(self):
        global c_process, d_process
        try:
            logger.info('starting proxypool...')
            c_process = multiprocessing.Process(target=self.crawler)
            c_process.start()
            logger.info(f'starting getter, pid {c_process.pid}')
            d_process = multiprocessing.Process(target=self.detector)
            d_process.start()
            logger.info(f'starting detector, pid {d_process.pid}')
            c_process.join()
            d_process.join()
            logger.info(f'crawler is {"alive" if c_process.is_alive() else "dead"}')
            logger.info(f'detector is {"alive" if d_process.is_alive() else "dead"}')
        except KeyboardInterrupt:
            logger.info('received keyboard interrupt signal')
            c_process and c_process.terminate()
            d_process and d_process.terminate()


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
