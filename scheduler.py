import time
import multiprocessing
from loguru import logger
from crawler import Crawler
from tester import Tester
from settings import GET_CYCLE, TEST_CYCLE


# 子进程句柄
getter_process, tester_process = None, None


class Scheduler:

    def getter(self, cycle=GET_CYCLE):
        c = Crawler()
        loop = 0
        while True:
            logger.info(f'getter loop {loop} start')
            c.run()
            loop += 1
            time.sleep(cycle)

    def tester(self, cycle=TEST_CYCLE):
        d = Tester()
        loop = 0
        while True:
            logger.info(f'tester loop {loop} start...')
            d.run()
            loop += 1
            time.sleep(cycle)

    def run(self):
        global getter_process, tester_process
        try:
            logger.info('starting proxypool...')
            getter_process = multiprocessing.Process(target=self.getter)
            getter_process.start()
            logger.info(f'starting getter, pid {getter_process.pid}')
            tester_process = multiprocessing.Process(target=self.tester)
            tester_process.start()
            logger.info(f'starting tester, pid {tester_process.pid}')
            getter_process.join()
            tester_process.join()
            logger.info(f'getter is {"alive" if getter_process.is_alive() else "dead"}')
            logger.info(f'tester is {"alive" if tester_process.is_alive() else "dead"}')
        except KeyboardInterrupt:
            logger.info('received keyboard interrupt signal')
            getter_process and getter_process.terminate()
            tester_process and tester_process.terminate()


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
