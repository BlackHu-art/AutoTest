#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    11:00
"""
import time
from common.logger.logTool import logger
from common.appium.remoteControlActions import RemoteControlActions
from page_objects.doozy_tv.elements.loadingPageElements import LoadingPageElements


class StartPage:
    def __init__(self, appOperator):
        self._appOperator = appOperator
        self._remoteControl = RemoteControlActions(self._appOperator.getDriver())
        self._loadingPageElements = LoadingPageElements()

    def getElements(self):
        return self._loadingPageElements
