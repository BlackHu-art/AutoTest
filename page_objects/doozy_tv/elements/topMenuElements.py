#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    10:57
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class TopMenuElements:
    def __init__(self):
        # top_container
        self.top_container = CreateElement.create(Locator_Type.ID, 'com.mm.droid.livetv.stb31023418:id/rl_menu',
                                                  wait_type=Wait_By.VISIBILITY_OF)
        self.product_logo_icon = CreateElement.create(Locator_Type.ID,
                                                      'com.mm.droid.livetv.stb31023418:id/menu_logo_icon',
                                                      wait_type=Wait_By.VISIBILITY_OF)
        self.top_menu_list_container = CreateElement.create(Locator_Type.ID,
                                                            'com.mm.droid.livetv.stb31023418:id/menu_list',
                                                            wait_type=Wait_By.VISIBILITY_OF)

        # home_menu_container
        self.home_menu_container = CreateElement.create(Locator_Type.XPATH,
                                                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.GridView/android.widget.RelativeLayout[1]',
                                                        wait_type=Wait_By.VISIBILITY_OF)
        self.home_menu_icon = CreateElement.create(Locator_Type.XPATH,
                                                   '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.GridView/android.widget.RelativeLayout[1]/android.widget.ImageView',
                                                   wait_type=Wait_By.VISIBILITY_OF)
        self.home_menu_text = CreateElement.create(Locator_Type.XPATH,
                                                   '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.GridView/android.widget.RelativeLayout[1]/android.widget.TextView',
                                                   wait_type=Wait_By.VISIBILITY_OF)

        # live_menu_container
        self.live_menu_container = CreateElement.create(Locator_Type.XPATH,
                                                        '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.GridView/android.widget.RelativeLayout[2]',
                                                        wait_type=Wait_By.VISIBILITY_OF)
        self.live_menu_icon = CreateElement.create(Locator_Type.XPATH,
                                                   '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.GridView/android.widget.RelativeLayout[2]/android.widget.ImageView',
                                                   wait_type=Wait_By.VISIBILITY_OF)
        self.live_menu_text = CreateElement.create(Locator_Type.XPATH,
                                                   '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.GridView/android.widget.RelativeLayout[2]/android.widget.TextView',
                                                   wait_type=Wait_By.VISIBILITY_OF)

        # replay_menu_container
        self.replay_menu_container = CreateElement.create(Locator_Type.XPATH,
                                                          '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.GridView/android.widget.RelativeLayout[3]',
                                                          wait_type=Wait_By.VISIBILITY_OF)
        self.replay_menu_icon = CreateElement.create(Locator_Type.XPATH,
                                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.GridView/android.widget.RelativeLayout[3]/android.widget.ImageView',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.replay_menu_text = CreateElement.create(Locator_Type.XPATH,
                                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.GridView/android.widget.RelativeLayout[3]/android.widget.TextView',
                                                     wait_type=Wait_By.VISIBILITY_OF)

        # search_menu_container
        self.search_menu_container = CreateElement.create(Locator_Type.XPATH,
                                                          '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.GridView/android.widget.RelativeLayout[4]',
                                                          wait_type=Wait_By.VISIBILITY_OF)
        self.search_menu_icon = CreateElement.create(Locator_Type.XPATH,
                                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.GridView/android.widget.RelativeLayout[4]/android.widget.ImageView',
                                                     wait_type=Wait_By.VISIBILITY_OF)
        self.search_menu_text = CreateElement.create(Locator_Type.XPATH,
                                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.GridView/android.widget.RelativeLayout[4]/android.widget.TextView',
                                                     wait_type=Wait_By.VISIBILITY_OF)

        # profile_menu_container
        self.profile_menu_container = CreateElement.create(Locator_Type.ID,'com.mm.droid.livetv.stb31023418:id/profile_ll',
                                                           wait_type=Wait_By.VISIBILITY_OF)
        self.profile_menu_icon = CreateElement.create(Locator_Type.ID,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.ImageView',
                                                      wait_type=Wait_By.VISIBILITY_OF)