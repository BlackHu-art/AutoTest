# -*- coding:utf8 -*-

from base.app_ui.android_Project_client import Android_Project_Client
from page_objects.doozy_tv.pages.startPage import StartPage
from common.logger.logTool import logger
import pytest


class TestCases:
    def setup_class(self):
        """Startpage页面 测试需要重置app"""
        self.demoProjectClient = Android_Project_Client(is_need_kill_app=True)
        self.startPage = StartPage(self.demoProjectClient.appOperator)

    """该函数为一个Pytest fixture，自动用于每个测试用例"""

    # @pytest.fixture(autouse=True)
    # def record_test_case_video(self):
    #     self.demoProjectClient.appOperator.start_recording_screen()
    #     yield self.record_test_case_video
    #     self.demoProjectClient.appOperator.stop_recording_screen()

    # @pytest.mark.run(order=1)
    # pytest顺序执行器

    @pytest.fixture
    def fixture_test(self):
        logger.info('\n......start......')
        yield self.fixture_test
        logger.info('\n...... end ......')

    @pytest.mark.run(order=3)
    def test_app(self, fixture_test):
        pass



    def teardown_class(self):
        pass
