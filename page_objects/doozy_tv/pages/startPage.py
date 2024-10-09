# -*- coding:utf-8 -*-
import time
from common.logger.logTool import logger
from common.appium.remoteControlActions import RemoteControlActions
from page_objects.doozy_tv.elements.startPageElements import StartPageElements


class StartPage:
    def __init__(self, appOperator):
        self.appOperator = appOperator
        self.remote_control = RemoteControlActions(self.appOperator.getDriver())
        self._startPageElements = StartPageElements()

    def is_allow_container_displayed(self):
        if self.appOperator.is_displayed(self._startPageElements.permission_container):
            self.appOperator.get_screenshot('dialog_container')
            logger.info('permission_container is displayed')
        else:
            logger.info('permission_container is not displayed')
            return False

    def click_allow_btn(self):
        self.is_allow_container_displayed()
        self.remote_control.press_down()
        self.appOperator.touch_tap(self._startPageElements.permission_allow_button)
        logger.info('touch_tap permission_allow_button')
        time.sleep(5)
        self.appOperator.get_screenshot('after_click_allow_btn')

    def click_deny_btn(self):
        self.is_allow_container_displayed()
        self.remote_control.press_down()
        self.remote_control.press_left()
        self.appOperator.touch_tap(self._startPageElements.permission_deny_button)
        logger.info('touch_tap permission_deny_button')
        time.sleep(5)
        self.appOperator.get_screenshot('after_click_deny_btn')

    def getElements(self):
        return self._startPageElements
