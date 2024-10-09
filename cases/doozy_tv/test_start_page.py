# -*- coding:utf8 -*-

from base.app_ui.android_Project_client import Android_Project_Client
from page_objects.doozy_tv.pages.startPage import StartPage
import pytest


class TestStartPage:
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

    @pytest.fixture
    def fixture_test(self):
        """
        该函数是一个PyTest测试夹具（fixture），名为fixture_test_silde：
            执行测试前打印“start......”；
            使用yield提供fixture对象给测试函数使用；
            测试完成后，打印“end......”。
        """
        print('start......')
        yield self.fixture_test
        print('end......')

    def test_click_allow_btn(self, fixture_test):
        self.demoProjectClient.appOperator.reset_app()
        self.startPage.click_allow_btn()

    def test_click_deny_btn(self):
        self.demoProjectClient.appOperator.reset_app()
        self.startPage.click_deny_btn()

    def teardown_class(self):
        self.demoProjectClient.appOperator.reset_app()
