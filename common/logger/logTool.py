#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author      :  Frankie
@description :  loguru 封装类，导入即可直接使用
                当前文件名 Logger.py
@time        :    10:14
"""

from functools import wraps
import sys
import datetime
import loguru
from pathlib import Path
import os
import configparser


def singleton_class_decorator(cls):
    _instance = {}

    @wraps(cls)
    def wrapper_class(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return wrapper_class


@singleton_class_decorator
class Logger:
    def __init__(self):
        self.logger_add()

    @staticmethod
    def read_ini():
        config = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))
        config.read(Path(Path(__file__).parent, 'log.ini'), encoding="UTF-8")
        return config

    @staticmethod
    def get_project_path(project_path=None):
        if project_path is None:
            project_path = Path(__file__).parent.parent
        return project_path

    def get_log_path(self):
        project_path = self.get_project_path()
        project_log_dir = Path(project_path, 'Logs')
        project_log_filename = f'{datetime.date.today()}.log'
        project_log_path = Path(project_log_dir, project_log_filename)

        os.makedirs(project_log_dir, exist_ok=True)
        return project_log_path

    def logger_add(self):
        loguru.logger.remove()

        config = self.read_ini()

        def get_level(section):
            return config.get(section, 'level')

        if config.get('StderrLog', 'is_open').lower() == "on":
            loguru.logger.add(
                sys.stderr,
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | "
                       "{thread.name} | <cyan>{module}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                       "<level>{message}</level>",
                level=get_level('StderrLog'),
            )

        if config.get('FileLog', 'is_open').lower() == "on":
            project_log_path = self.get_log_path()
            loguru.logger.add(
                sink=str(project_log_path),
                rotation=config.get('FileLog', 'rotation'),
                retention=config.get('FileLog', 'retention'),
                compression='zip',
                encoding="utf-8",
                enqueue=True,
                format="[{time:YYYY-MM-DD HH:mm:ss} {level:<8} | {file}:{module}.{function}:{line}]  {message}",
                level=get_level('FileLog'),
            )

    @property
    def get_logger(self):
        return loguru.logger


# 实例化日志类
logger = Logger().get_logger

if __name__ == '__main__':
    logger.debug('this is a debug message')
    logger.info('this is an info message')
    logger.warning('this is a warning message')
    logger.error('this is an error message')
    logger.success('this is a success message')
    logger.critical('this is a critical message')
