#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    16:52
"""

from appium.webdriver.webdriver import WebDriver
from common.logger.logTool import logger


class TvRemoteOperator:
    """
    遥控器操作点击方式封装
    """

    def __init__(self, driver: WebDriver):
        """
        初始化Appium驱动以控制电视设备
        """
        self._driver = driver

    def press_key(self, key_code):
        """
        按下指定的按键，使用Android KeyEvent API。
        :param key_code: 按键的键值代码（KeyEvent）
        """
        self._driver.press_keycode(key_code)
        logger.info(f'按下了按键：{key_code}')

    # 基本遥控器功能封装
    def press_up(self):
        """模拟遥控器向上按键"""
        self.press_up()  # KEYCODE_DPAD_UP
        logger.info('KEYCODE_DPAD_UP')

    def press_down(self):
        """模拟遥控器向下按键"""
        self.press_down()  # KEYCODE_DPAD_DOWN
        logger.info('KEYCODE_DPAD_DOWN')

    def press_left(self):
        """模拟遥控器向左按键"""
        self.press_left()  # KEYCODE_DPAD_LEFT
        logger.info('KEYCODE_DPAD_LEFT')

    def press_right(self):
        """模拟遥控器向右按键"""
        self.press_right()  # KEYCODE_DPAD_RIGHT
        logger.info('KEYCODE_DPAD_RIGHT')

    def press_ok(self):
        """模拟遥控器确认/选择按键"""
        self.press_ok()  # KEYCODE_DPAD_CENTER
        logger.info('KEYCODE_DPAD_CENTER')

    def press_back(self):
        """模拟返回按键"""
        self.press_back()  # KEYCODE_BACK
        logger.info('KEYCODE_BACK')

    def press_home(self):
        """模拟主页按键"""
        self.press_home()  # KEYCODE_HOME
        logger.info('KEYCODE_HOME')

    def press_menu(self):
        """模拟菜单按键"""
        self.press_menu()  # KEYCODE_MENU
        logger.info('KEYCODE_MENU')

    # 音量控制功能
    def volume_up(self):
        """增加音量"""
        self.volume_up()  # KEYCODE_VOLUME_UP
        logger.info('KEYCODE_VOLUME_UP')

    def volume_down(self):
        """降低音量"""
        self.volume_down()  # KEYCODE_VOLUME_DOWN
        logger.info('KEYCODE_VOLUME_DOWN')

    def mute(self):
        """静音"""
        self.mute()  # KEYCODE_MUTE

    # 其他常用按键
    def power(self):
        """模拟电源开/关按键"""
        self.power()  # KEYCODE_POWER

    def close(self):
        """关闭Appium会话"""
        if self._driver:
            self._driver.quit()

