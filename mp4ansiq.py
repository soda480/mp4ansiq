import os
import sys
import time
import logging
from multiprocessing import Queue
from queue import Empty
from mp4ansi import MP4ansi

logger = logging.getLogger(__name__)

BACKGROUND_PROCESSES = 15
AMOUNT_OF_WORK = 100


def configure_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    name = os.path.basename(sys.argv[0]).replace('.py', '')
    file_handler = logging.FileHandler(f'{name}.log')
    file_formatter = logging.Formatter("%(asctime)s %(processName)s %(name)s [%(funcName)s] %(levelname)s %(message)s")
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)


def prepare_queue(amount):
    queue = Queue()
    for index in range(amount):
        queue.put({'item': f'item{index}'})
    return queue


def get_process_data(processes, amount):
    queue = prepare_queue(amount)
    process_data = []
    for process in range(processes):
        process_data.append({'queue': queue, 'process': process})
        # process_data.append({'process': process})
    return process_data


def run_q(process_data, shared_data):
    queue = process_data['queue']
    # queue = shared_data['queue']
    process = process_data['process']
    results = []
    while True:
        try:
            qitem = queue.get(timeout=2)
            item = qitem['item']
            # sleep to simulate work
            logger.debug(f'processing {item}')
            time.sleep(.5)
            results.append(f'process {process} processed item {item}')
        except Empty:
            logger.debug('queue is empty')
            break
    logger.debug('processing complete')
    return results


def log_results(process_data):
    logger.debug('here is who did what')
    for process in process_data:
        for result in process['result']:
            logger.debug(result)


def run():
    print(f'Starting {BACKGROUND_PROCESSES} background processes to process {AMOUNT_OF_WORK} items')
    mp4ansi = MP4ansi(
        function=run_q,
        process_data=get_process_data(BACKGROUND_PROCESSES, AMOUNT_OF_WORK),
        # it is better to pass queue to workers using shared data instead of process data as there
        # will be less references this way but keeping it this way to be consistent with previous example
        # shared_data={'queue': prepare_queue(AMOUNT_OF_WORK)},
        config={'text_regex': r'.*processing.*'})
    mp4ansi.execute(raise_if_error=True)
    log_results(mp4ansi.process_data)


def main():
    configure_logging()
    try:
        run()
    except Exception as exception:
        logger.error(exception)
        print(f'ERROR: {exception}')
        sys.exit(1)


if __name__ == '__main__':

    main()
