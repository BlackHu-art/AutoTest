#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    10:28
"""
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from page_objects.doozy_tv.locator_type import Locator_Type


class HomePageElements:
    def __init__(self):
        self.home_loading_container = CreateElement.create(Locator_Type.ID,
                                                           'com.mm.droid.livetv.stb31023418:id/liveloadf_ll_loading',
                                                           wait_type=Wait_By.VISIBILITY_OF)
        self.home_loading_icon = CreateElement.create(Locator_Type.ID,
                                                      '	com.mm.droid.livetv.stb31023418:id/liveloadf_slv',
                                                      wait_type=Wait_By.VISIBILITY_OF)
        self.home_loading_text = CreateElement.create(Locator_Type.ID,
                                                      'com.mm.droid.live tv.stb31023418:id/liveloadf_tv_loading_text',
                                                      wait_type=Wait_By.VISIBILITY_OF)
