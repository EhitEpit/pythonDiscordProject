import logging
import time
import platform
import os


class Log:
    def __init__(self, class_name=''):
        self.logger = logging.getLogger(class_name)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        if platform.system() == 'Windows':
            if not os.path.exists(os.getcwd() + '\\log'):
                os.mkdir(os.getcwd() + '\\log')
            file_handler = logging.FileHandler("log\\" + class_name + time.strftime('%Y%m%d', time.localtime()) + ".log")
        else:
            if not os.path.exists(os.getcwd() + '/log'):
                os.mkdir(os.getcwd() + '/log')
            file_handler = logging.FileHandler("log/" + class_name + time.strftime('%Y%m%d', time.localtime()) + ".log")
        self.logger.addHandler(file_handler)

        self.logger.info("================Log Start================")

    def info(self, msg=''):
        self.logger.info(msg)

    def debug(self, msg=''):
        self.logger.debug(msg)

    def warning(self, msg=''):
        self.logger.warning(msg)

    def error(self, msg=''):
        self.logger.error(msg)
