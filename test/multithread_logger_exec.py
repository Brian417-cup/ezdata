import logging
import sys
import os
import os.path as osp
import threading
import uuid
import textwrap


def init_logger(filename, logger_name):
    import datetime

    '''
    @brief:
        initialize logger that redirect info to a file just in case we lost connection to the notebook
    @params:
        filename: to which file should we log all the info
        logger_name: an alias to the logger
    '''

    # logging.basicConfig(
    #     level=logging.INFO,
    #     # format='[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    #     format='%(message)s',
    #     handlers=[
    #         logging.FileHandler(filename=filename, encoding='utf-8'),
    #         logging.StreamHandler(sys.stdout)
    #     ],
    # )

    # Test
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')

    # 1. filehandler
    fh = logging.FileHandler(filename=filename, encoding='utf-8')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # 2. streamhandler
    ph = logging.StreamHandler(sys.stdout)
    ph.setLevel(logging.INFO)
    ph.setFormatter(formatter)
    logger.addHandler(ph)

    logger.info('### Init. Logger {} ###'.format(logger_name))
    return logger


def register_log_info(no):
    '''
    :return:
    '''
    import time
    os.makedirs('logs', exist_ok=True)
    log_path = osp.join('logs', time.strftime('%m%d_%H%M_%S_') + f'test_{no}.log')
    logger = init_logger(log_path, f'my_logger_{no}')
    return logger


#
# class CustomThread(threading.Thread):
#     def __init__(self, number: int):
#         threading.Thread.__init__(self)
#         self.no = number
#
#     def run(self) -> None:
#         def test_job(no):
#             logger = register_log_info(no)
#             code_str = '''
#                 import time
#                 logger.info(f"第{number}个子线程启动")
#                 logger.info("测试的第一个字段")
#                 print('控制台打印的字段')
#                 logger.info("测试的第二个字段")
#             '''
#
#             exec(textwrap.dedent(code_str), {'logger': logger, 'print': logging.info, 'number': no})
#
#         test_job(self.no)
#
#     def execute(self):
#         self.start()
#
#
# for i in range(20):
#     CustomThread(i).execute()


def test_job(no):
    logger = register_log_info(no)
    code_str = '''
        import time
        logger.info(f"第{number}个子线程启动")
        logger.info("测试的第一个字段")
        print('控制台打印的字段')
        logger.info("测试的第二个字段")
    '''

    exec(textwrap.dedent(code_str), {'logger': logger, 'print': logger.info, 'number': no})


# 创建并启动多个线程
threads = []
for i in range(5):  # 假设启动5个线程
    thread_name = f"Thread-{i + 1}"
    t = threading.Thread(target=test_job, args=(i + 1,))
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()
