#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    20:29
"""
from common.appium.tvRemoteOperator import TvRemoteOperator
from common.logger.logTool import logger


class RemoteControlActions:
    def __init__(self, driver):
        self.driver = driver

    def press_button(self, key_code):
        logger.info(f'Pressing key code: {key_code}')
        self.driver.press_keycode(key_code)

    def press_up(self):
        logger.info('ARROW_UP')
        self.press_button(TvRemoteOperator.UP)

    def press_down(self):
        logger.info('ARROW_DOWN')
        self.press_button(TvRemoteOperator.DOWN)

    def press_left(self):
        logger.info('ARROW_LEFT')
        self.press_button(TvRemoteOperator.LEFT)

    def press_right(self):
        logger.info('ARROW_RIGHT')
        self.press_button(TvRemoteOperator.RIGHT)

    def press_center(self):
        logger.info('OK_BUTTON')
        self.press_button(TvRemoteOperator.CENTER)

    def press_back(self):
        logger.info('BACK_BUTTON')
        self.press_button(TvRemoteOperator.BACK)

    # 其他按键调用...
