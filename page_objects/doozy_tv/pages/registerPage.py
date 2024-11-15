#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    13:45
"""
from common.logger.logTool import logger
from common.yamlTool import YamlTool
from common.appium.remoteControlActions import RemoteControlActions
from page_objects.doozy_tv.elements.registerPageElements import RegisterPageElements
from page_objects.doozy_tv.elements.topMenuElements import TopMenuElements
from page_objects.doozy_tv.elements.profilePageElements import ProfilePageElements
from page_objects.doozy_tv.elements.loginMethodPageElements import LoginMethodPageElements


class RegisterPage:
    def __init__(self, _appOperator):
        self._appOperator = _appOperator
        self._remoteControl = RemoteControlActions(self._appOperator.getDriver())
        self.registerPageElements = RegisterPageElements()
        self.topMenuElements = TopMenuElements()
        self.profilePageElements = ProfilePageElements()
        self.loginMethodPageElements = LoginMethodPageElements()

    def click_back_btn(self):
        self._remoteControl.press_back()
        logger.info('Click back button')

    def move_to_register_email_element(self):
        if self._appOperator.is_displayed(self.registerPageElements.register_email_element):
            self._appOperator.move_cursor_to_element(self.registerPageElements.register_email_element)
            if self._appOperator.is_selected(self.registerPageElements.register_email_element):
                logger.info('Move to register email element')
                self._appOperator.get_screenshot('Move to register email element')

    def move_to_email_input_element(self):
        if self._appOperator.is_displayed(self.registerPageElements.register_email_input_text):
            self._appOperator.move_cursor_to_element(self.registerPageElements.register_email_input_text)
            logger.info('Move to email input element')
            self._appOperator.get_screenshot('Move to email input element')
            if self._appOperator.is_selected(self.registerPageElements.register_email_input_text):
                logger.info('Email input element is selected')

    def input_register_email(self, email):
        self._appOperator.input_text(self.registerPageElements.register_email_input_text, email)

    def move_to_register_phone_element(self):
        if self._appOperator.is_displayed(self.registerPageElements.register_phone_element):
            self._appOperator.move_cursor_to_element(self.registerPageElements.register_phone_element)
            logger.info('Move to register phone element')
            self._appOperator.get_screenshot('Move to register phone element')
