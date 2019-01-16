# -*- coding: utf-8 -*-

import logging
import logging.config
import os


class MyLogging(object):

    def init(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
        conf_dir = os.path.join(parent_dir, "conf")

        # 初始化日志类
        log_conf = os.path.join(conf_dir, "logger.config")
        logging.config.fileConfig(log_conf)

    def get_logger(self, logger_name):
        return logging.getLogger(logger_name)
