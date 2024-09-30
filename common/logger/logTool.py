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
from loguru import logger as loguru_logger
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
    """
    日志封装类，使用 loguru 进行日志记录，支持读取配置文件。
    """

    def __init__(self):
        self.config = self.read_ini()
        self.project_path = self.get_project_path()  # 初始化项目路径
        self.logger_add()  # 初始化日志配置

    @staticmethod
    def read_ini():
        """
        读取日志配置文件log.ini。
        :return: configparser对象
        """
        config = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))
        try:
            ini_path = Path(Path(__file__).parent, 'log.ini')
            if ini_path.exists():
                config.read(ini_path, encoding="utf-8")
            else:
                loguru_logger.error(f"配置文件未找到: {ini_path}")
        except Exception as e:
            loguru_logger.error(f"读取配置文件失败: {e}")
        return config

    @staticmethod
    def get_project_path():
        """
        获取项目根路径。
        :return: 项目根目录路径
        """
        return Path(__file__).parent.parent

    def get_log_path(self):
        """
        获取日志文件路径。
        :return: 日志文件的绝对路径
        """
        project_log_dir = Path(self.project_path, 'Logs')
        project_log_filename = f'{datetime.date.today()}.log'
        project_log_path = Path(project_log_dir, project_log_filename)

        try:
            project_log_dir.mkdir(parents=True, exist_ok=True)  # 创建日志目录
        except Exception as e:
            loguru_logger.error(f"创建日志目录失败: {e}")
        return project_log_path

    def logger_add(self):
        """
        配置 loguru 日志输出，包含标准输出和文件输出。
        """
        loguru_logger.remove()

        # 从配置文件获取日志级别
        def get_level(section):
            return self.config.get(section, 'level', fallback='INFO')

        # 标准输出日志
        if self.config.get('StderrLog', 'is_open', fallback='off').lower() == "on":
            loguru_logger.add(
                sys.stderr,
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | "
                       "{thread.name} | <cyan>{module:<10}</cyan>.<cyan>{function:<10}</cyan>:<cyan>{line:<5}</cyan> | "
                       "<level>{message}</level>",
                level=get_level('StderrLog'),
            )

        # 文件输出日志
        if self.config.get('FileLog', 'is_open', fallback='off').lower() == "on":
            project_log_path = self.get_log_path()
            loguru_logger.add(
                sink=str(project_log_path),
                rotation=self.config.get('FileLog', 'rotation', fallback="1 week"),
                retention=self.config.get('FileLog', 'retention', fallback="1 month"),
                compression='zip',
                encoding="utf-8",
                enqueue=True,
                format="[{time:YYYY-MM-DD HH:mm:ss} {level:<8} | {file}:{module}.{function}:{line}]  {message}",
                level=get_level('FileLog'),
            )

    @property
    def get_logger(self):
        """
        获取 loguru logger 实例。
        :return: loguru.logger
        """
        return loguru_logger


# 实例化日志类
logger = Logger().get_logger

if __name__ == '__main__':
    logger.debug('this is a debug message')
    logger.info('this is an info message')
    logger.warning('this is a warning message')
    logger.error('this is an error message')
    logger.success('this is a success message')
    logger.critical('this is a critical message')
