#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :
 @time        :  2024/10/15 16:53
"""
from base.app_ui.android_Project_read_config import APP_UI_Android_DemoProject_Read_Config
from appium import webdriver
from base.read_app_ui_config import Read_APP_UI_Config
from common.appium.appOperator import AppOperator
from common.fileTool import FileTool
from common.httpclient.doRequest import DoRequest
from common.logger.logTool import logger
from init.app_ui.android.demoProject.demoProjectInit import DemoProjectInit
import os


class Android_Project_Client(object):
    __instance = None
    __inited = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, is_need_reset_app=False, is_need_kill_app=False):
        """在首次调用时初始化"""
        if self.__inited is None:
            # 标记为已初始化，确保只初始化一次
            self.__inited = True
            self.__is_first = True
            # 读取配置
            self.config = Read_APP_UI_Config().app_ui_config
            self.device_info = FileTool.readJsonFromFile('config/app_ui_tmp/' + str(os.getppid()))
            self.demoProject_config = APP_UI_Android_DemoProject_Read_Config(
                'config/doozy_tv/%s' % self.device_info['app_ui_config']).config
            self.current_desired_capabilities = FileTool.readJsonFromFile(
                'config/app_ui_tmp/' + str(os.getppid()) + '_current_desired_capabilities')
            self.fullReset = self.current_desired_capabilities['fullReset']
            self.noReset = self.current_desired_capabilities['noReset']
            self._appium_hub = 'http://' + self.device_info['server_ip'] + ':%s/wd/hub' % self.device_info[
                'server_port']
            self._init(self.demoProject_config.init)
            self._delete_last_device_session(self.device_info['device_desc'])
            self.driver = webdriver.Remote(self._appium_hub, desired_capabilities=self.current_desired_capabilities)
            self._save_last_device_session(self.driver.session_id, self.device_info['device_desc'])
            self.appOperator = AppOperator(self.driver, self._appium_hub)

        if is_need_reset_app:
            # appium启动是非重置或者非第一次appium启动，则要进行重置
            if self.__is_first == False or self.noReset == True:
                logger.warning('is_need_reset_app is True, reset app')
                self.appOperator.reset_app()
        elif is_need_kill_app:
            # appium启动是非重置或者非第一次appium启动，则要进行重启进程
            if self.__is_first == False or self.noReset == True:
                appPackage = self.current_desired_capabilities['appPackage']
                appActivity = self.current_desired_capabilities['appActivity']
                logger.warning('is_need_kill_app is True, restart app')
                self.appOperator.start_activity(appPackage, appActivity)

        self.__is_first = False

    def _init(self, is_init=False):
        print('初始化android基础数据......')
        DemoProjectInit().init(is_init)
        print('初始化android基础数据完成......')

    def _save_last_device_session(self, session, device_desc):
        if not os.path.exists('config/app_ui_tmp'):
            os.mkdir('config/app_ui_tmp')
            with open('config/app_ui_tmp/%s_session' % device_desc, 'w') as f:
                f.write(session)
                f.close()

    def _delete_last_device_session(self, device_desc):
        if os.path.exists('config/app_ui_tmp/%s_session' % device_desc):
            with open('config/app_ui_tmp/%s_session' % device_desc, 'r') as f:
                last_session = f.read()
                last_session = last_session.strip()
                if last_session:
                    doRequest = DoRequest(self._appium_hub)
                    doRequest.setHeaders({'Content-Type': 'application/json'})
                    httpResponseResult = doRequest.delete('/session/' + last_session)
