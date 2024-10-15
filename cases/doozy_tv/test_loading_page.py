#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    11:00
"""
from base.app_ui.android_Project_client import Android_Project_Client
from page_objects.doozy_tv.pages.loadingPage import LoadingPage
from common.logger.logTool import logger
import pytest


class TestLoadingPage:
    def setup_class(self):
        self.demoProjectClient = Android_Project_Client(is_need_kill_app=True)
        self.loadingPage = LoadingPage(self.demoProjectClient.appOperator)

    @pytest.fixture
    def fixture_test(self):
        logger.info('\n......start......')
        yield self.fixture_test
        logger.info('\n...... end ......')

    @pytest.mark.run(order=3)
    def test_restart_app(self, fixture_test):
        self.loadingPage.found_loading_container()

    def teardown_class(self):
        pass
