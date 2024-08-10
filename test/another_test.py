import logging
import threading
import sys


class PrintLogger:
    def __init__(self, logger):
        self.logger = logger

    def write(self, message):
        if message.strip():  # 避免记录空行
            self.logger.info(message.strip())

    def flush(self):
        pass  # 不需要实现，保持空即可


def create_logger(thread_name):
    # 创建 logger
    logger = logging.getLogger(thread_name)
    logger.setLevel(logging.DEBUG)

    # 创建文件处理器，每个线程的日志记录在不同的文件中
    fh = logging.FileHandler(f'{thread_name}.log')
    fh.setLevel(logging.DEBUG)

    # 创建日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # 将文件处理器添加到 logger
    logger.addHandler(fh)

    return logger


def thread_function(name, number):
    logger = create_logger(name)

    # 重定向 print 到 logger
    sys.stdout = PrintLogger(logger)

    logger.info(f"第{number}个子线程启动")
    logger.info("测试的第一个字段")
    print('控制台打印的字段')
    logger.info("测试的第二个字段")


# 创建并启动多个线程
threads = []
for i in range(3):  # 假设启动3个线程
    thread_name = f"Thread-{i + 1}"
    t = threading.Thread(target=thread_function, args=(thread_name, i + 1))
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()
