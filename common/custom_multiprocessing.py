#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :
 @time        :  2024/9/27 15:26
"""
from multiprocessing.pool import Pool
import multiprocessing


class NoDaemonProcess(multiprocessing.Process):
    """重构multiprocessing.Process类，将进程始终定义为非守护进程

    Args:
        multiprocessing (_type_): _description_

    Returns:
        _type_: _description_
    """

    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, value):
        pass


class NoDaemonContext(type(multiprocessing.get_context())):
    Process = NoDaemonProcess


class Custom_Pool(Pool):
    """重构multiprocessing.Pool类

    Args:
        Pool (_type_): _description_
    """

    def __init__(self, *args, **kwargs):
        kwargs['context'] = NoDaemonContext()
        super(Custom_Pool, self).__init__(*args, **kwargs)
