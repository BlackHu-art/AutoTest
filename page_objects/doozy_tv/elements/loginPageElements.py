#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    14:28
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class LoginPageElements:
    def __init__(self):
        # tv_notice
        self.login_notice_id = CreateElement.create(Locator_Type.ID,
                                                    'com.mm.droid.livetv.stb31023418:id/loada_tv_notice',
                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.login_notice_xpath = CreateElement.create(Locator_Type.XPATH,
                                                       '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.TextView',
                                                       wait_type=Wait_By.VISIBILITY_OF)
        # login_back_btn
        self.login_back_btn = CreateElement.create(Locator_Type.ID,
                                                   'com.mm.droid.livetv.stb31023418:id/loginf_iv_back',
                                                   wait_type=Wait_By.VISIBILITY_OF)

        # login_welcome_info_container
        self.login_container = CreateElement.create(Locator_Type.XPATH,
                                                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout[1]',
                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.login_logo_icon = CreateElement.create(Locator_Type.ID,
                                                    'com.mm.droid.livetv.stb31023418:id/menu_logo_icon',
                                                    wait_type=Wait_By.VISIBILITY_OF)
        self.login_welcome_title_text = CreateElement.create(Locator_Type.ID,
                                                             'com.mm.droid.livetv.stb31023418:id/welcomef_tv_welcome',
                                                             wait_type=Wait_By.VISIBILITY_OF)
        self.login_welcome_tips_text = CreateElement.create(Locator_Type.ID,
                                                            'com.mm.droid.livetv.stb31023418:id/welcomef_tv_remind',
                                                            wait_type=Wait_By.VISIBILITY_OF)

        # login_btn_container
        self.login_btn_container = CreateElement.create(Locator_Type.XPATH,
                                                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout[2]',
                                                        wait_type=Wait_By.VISIBILITY_OF)
        self.login_agreement_show_btn = CreateElement.create(Locator_Type.ID,
                                                             'com.mm.droid.livetv.stb31023418:id/agreement_show',
                                                             wait_type=Wait_By.VISIBILITY_OF)
        self.login_login_with_btn = CreateElement.create(Locator_Type.ID,
                                                         'com.mm.droid.livetv.stb31023418:id/account_login_tv2',
                                                         wait_type=Wait_By.VISIBILITY_OF)
        self.login_sign_up_btn = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/sign_up_tv2',
                                                      wait_type=Wait_By.VISIBILITY_OF)
