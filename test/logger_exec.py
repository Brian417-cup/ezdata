import logging
import sys
import os
import os.path as osp


def init_logger(filename, logger_name):
    import datetime

    '''
    @brief:
        initialize logger that redirect info to a file just in case we lost connection to the notebook
    @params:
        filename: to which file should we log all the info
        logger_name: an alias to the logger
    '''

    # get current timestamp
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d_%H-%M-%S')

    logging.basicConfig(
        level=logging.INFO,
        # format='[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        format='%(message)s',
        handlers=[
            logging.FileHandler(filename=filename, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ],
    )

    # Test
    logger = logging.getLogger(logger_name)
    logger.info('### Init. Logger {} ###'.format(logger_name))
    return logger


def register_log_info():
    '''
    :return:
    '''
    import time

    log_path = osp.join(time.strftime('%m%d_%H%M_%S_') + f'test.log')
    logger = init_logger(log_path, 'my_logger')
    return logger


code_str = '''
import time
logger.info("测试的第一个字段")
print('控制台打印的字段')
time.sleep(100)
logger.info("测试的第二个字段")
'''

logger = register_log_info()

exec(code_str, {'logger': logger, 'print': logging.info})
