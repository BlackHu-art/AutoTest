# -*- coding:utf-8 -*-
from common.logger.logTool import logger
from page_objects.doozy_tv.elements.startPageElements import StartPageElements


class StartPage:
    def __init__(self, appOperator):
        self.appOperator = appOperator
        self._startPageElements = StartPageElements()

    def is_allow_container_displayed(self):
        if self.appOperator.is_displayed(self._startPageElements.permission_container):
            self.appOperator.get_screenshot('dialog_container')
            logger.info('permission_container is displayed')
            return True
        else:
            logger.info('permission_container is not displayed')
            return False

    def click_allow_btn(self):
        self.appOperator.touch_tap(self._startPageElements.permission_allow_button)
        logger.info('touch_tap permission_allow_button')

    def click_deny_btn(self):
        self.appOperator.click(self._startPageElements.permission_deny_button)
        logger.info('click permission_deny_button')

    def getElements(self):
        return self._startPageElements
