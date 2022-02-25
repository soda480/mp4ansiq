import os
import sys
import time
import logging
from multiprocessing import Queue
from queue import Empty
from mp4ansi import MP4ansi

logger = logging.getLogger(__name__)

BACKGROUND_PROCESSES = 15


def configure_logging():
    """ configure logging and logfile
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    name = os.path.basename(sys.argv[0]).replace('.py', '')
    file_handler = logging.FileHandler(f'{name}.log')
    file_formatter = logging.Formatter("%(asctime)s %(processName)s %(name)s [%(funcName)s] %(levelname)s %(message)s")
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)


def prepare_queue():
    queue = Queue()
    for index in range(100):
        queue.put({'item': f'item{index}'})
    return queue


def get_process_data(processes):
    queue = prepare_queue()
    process_data = []
    for process in range(processes):
        process_data.append({'queue': queue, 'process': process})
    return process_data


def run_q(process_data, *args):
    queue = process_data['queue']
    process = process_data['process']
    results = []
    while True:
        try:
            qitem = queue.get(timeout=2)
            item = qitem['item']
            logger.debug(f'processing {item}')
            # simulate work
            time.sleep(.5)
            results.append(f'process {process} processed item {item}')
        except Empty:
            logger.debug('queue is empty')
            break
    logger.debug('processing complete')
    return results


def log_results(process_data):
    logger.debug('here are the results')
    results = []
    for process in process_data:
        results.extend(process['result'])
        for result in process['result']:
            logger.debug(result)


def run():
    print(f'Starting {BACKGROUND_PROCESSES} background processes to process items')
    process_data = get_process_data(BACKGROUND_PROCESSES)
    config = {'text_regex': r'.*processing.*'}
    mp4ansi = MP4ansi(
        function=run_q,
        process_data=process_data,
        config=config)
    mp4ansi.execute(raise_if_error=True)
    log_results(mp4ansi.process_data)


def main():
    """ main function
    """
    configure_logging()
    try:
        run()
    except Exception as exception:
        logger.error(exception)
        print(f'ERROR: {exception}')
        sys.exit(1)


if __name__ == '__main__':
    main()
