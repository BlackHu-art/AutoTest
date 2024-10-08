# -*- coding:utf8 -*-

from base.app_ui.android_Project_client import Android_Project_Client
from page_objects.doozy_tv.pages.startPage import StartPage
import pytest
import time


class TestIndexPage:
    def setup_class(self):
        self.demoProjectClient = Android_Project_Client(is_need_kill_app=True)
        self.startPage = StartPage(self.demoProjectClient.appOperator)
        self.startPage.click_start()
        self.indexPage = self.startPage.choice_a_city()
        self.appOperator = self.demoProjectClient.appOperator

    @pytest.fixture(autouse=True)
    def record_test_case_video(self):
        self.appOperator.start_recording_screen()
        yield self.record_test_case_video
        self.appOperator.stop_recording_screen()

    @pytest.fixture
    def fixture_test_silde(self):
        print('start......')
        yield self.fixture_test_silde
        print('end......')

    def test_silde(self, fixture_test_silde):
        time.sleep(10)
        self.indexPage.index_left_silde()
        self.indexPage.index_right_silde()
        self.indexPage.index_up_silde()
        self.indexPage.index_down_silde()

    def teardown_class(self):
        self.appOperator.reset_app()
