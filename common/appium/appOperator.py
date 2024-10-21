#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :
 @time        :  2024/10/8 16:53
"""

from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from common.dateTimeTool import DateTimeTool
from common.httpclient.doRequest import DoRequest
from common.logger.logTool import logger
from page_objects.createElement import CreateElement
from page_objects.doozy_tv.locator_type import Locator_Type
from page_objects.doozy_tv.wait_type import Wait_Type as Wait_By
from selenium.webdriver.common.by import By
from pojo.elementInfo import ElementInfo
from PIL import Image

import allure
import base64
import ujson
import os


class AppOperator:
    """
    类中的element参数可以有appium.webdriver.webelement.WebElement和pojo.elementInfo.ElementInfo类型
    """

    def __init__(self, driver: WebDriver, appium_hub):
        self._doRequest = DoRequest(appium_hub)
        self._doRequest.setHeaders({'Content-Type': 'application/json'})
        self._driver = driver
        self._session_id = driver.session_id
        # 获得设备支持的性能数据类型
        self._performance_types = ujson.loads(
            self._doRequest.post_with_form('/session/' + self._session_id + '/appium/performanceData/types').body)[
            'value']
        # 获取当前窗口大小
        self._window_size = self.get_window_size()
        # 获得当前窗口的位置
        self._window_rect = self.get_window_rect()

    def _change_element_to_webElement_type(self, element):
        if isinstance(element, ElementInfo):
            webElement = self.getElement(element)
        elif isinstance(element, WebElement):
            webElement = element
        else:
            return element
        return webElement

    def get(self, url):
        self._driver.get(url)

    def get_current_url(self):
        return self._driver.current_url

    def getTitle(self):
        return self._driver.title

    def getText(self, element):
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            return webElement.text

    def click(self, element):
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            webElement.click()

    def submit(self, element):
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            webElement.submit()

    def sendText(self, element, text):
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            webElement.clear()
            webElement.send_keys(text)

    def is_displayed(self, element):
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            flag = webElement.is_displayed()
            return flag

    def is_enabled(self, element):
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            flag = webElement.is_enabled()
            return flag

    def is_selected(self, element):
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            flag = webElement.is_selected()
            return flag

    def get_screenshot(self, fileName):
        fileName = DateTimeTool.getNowTime('%Y%m%d%H%M%S%f_') + fileName
        allure.attach(name=fileName, body=self._driver.get_screenshot_as_png(),
                      attachment_type=allure.attachment_type.PNG)

    def refresh(self):
        self._driver.refresh()

    def get_property(self, element, property_name):
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            return webElement.get_property(property_name)

    def get_attribute(self, element, attribute_name):
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            return webElement.get_attribute(attribute_name)

    def get_element_outer_html(self, element):
        return self.get_attribute(element, 'outerHTML')

    def get_element_inner_html(self, element):
        return self.get_attribute(element, 'innerHTML')

    def get_page_source(self):
        """
        获得app的层次结构xml，web页面源码
        """
        return self._driver.page_source

    def get_element_rgb(self, element, x_percent=0, y_percent=0):
        """
        获得元素上的rgb值,默认返回元素左上角坐标轴
        :param element
        :param x_percent x轴百分比位置,范围0~1
        :param y_percent y轴百分比位置,范围0~1
        """
        img = Image.open(self.save_element_image(element, 'element_rgb'))
        pix = img.load()
        width = img.size[0]
        height = img.size[1]
        point_rgb = pix[width * x_percent, height * y_percent]
        point_rgb = point_rgb[:3]
        return point_rgb

    def save_element_image(self, element, image_file_name):
        """
        截取元素图片
        :param image_file_name: 保存图片的文件名
        :return: 图片存储的路径
        """
        webElement = self._change_element_to_webElement_type(element)
        webElement_x = webElement.location['x']
        webElement_y = webElement.location['y']
        webElement_width = webElement.size['width']
        webElement_height = webElement.size['height']
        window_x = self._window_rect['x']
        window_y = self._window_rect['y']
        window_width = self._window_rect['width']
        window_height = self._window_rect['height']
        left_percent = webElement_x / window_width
        top_percent = webElement_y / window_height
        right_percent = (webElement_x + webElement_width) / window_width
        bottom_percent = (webElement_y + webElement_height) / window_height
        # 进行屏幕截图
        image_file_name = DateTimeTool.getNowTime('%Y%m%d%H%M%S%f_') + '%s.png' % image_file_name
        if not os.path.exists('output/tmp/'):
            os.mkdir('output/tmp/')
        image_file_name = os.path.abspath('output/tmp/' + image_file_name)
        self._driver.get_screenshot_as_file(image_file_name)
        img = Image.open(image_file_name)
        # 裁切应用区域图片并保存
        img = img.crop((window_x, window_y, window_x + window_width, window_y + window_height))
        img.save(image_file_name)
        img_size = img.size
        img_width = img_size[0]
        img_height = img_size[1]
        # 裁切元素区域图片并保存
        img = img.crop((left_percent * img_width, top_percent * img_height, right_percent * img_width,
                        bottom_percent * img_height))
        img.save(image_file_name)
        return image_file_name

    def get_captcha(self, element, language='eng'):
        """
        识别图片验证码，如需使用该方法必须配置jpype1、字体库等依赖环境
        :param element: 验证码图片元素
        :param language: eng:英文,chi_sim:中文
        :return:
        """
        # 识别图片验证码
        from common.captchaRecognitionTool import CaptchaRecognitionTool
        captcha_image_file_name = self.save_element_image(element, 'captcha')
        captcha = CaptchaRecognitionTool.captchaRecognition(captcha_image_file_name, language)
        captcha = captcha.strip()
        captcha = captcha.replace(' ', '')
        return captcha

    def get_window_size(self):
        return self._driver.get_window_size()

    def get_window_rect(self):
        return self._driver.get_window_rect()

    def app_alert(self, platformName, action_type='accept', buttonLabel=None):
        """
        仅适用于app
        :platformName android、ios
        :action_type accept、dismiss
        :buttonLabel
        :return:
        """
        if action_type:
            action_type.lower()
        if platformName:
            platformName.lower()
        script = None
        script_arg = {}
        if buttonLabel:
            script_arg.update({'buttonLabel': buttonLabel})
        if platformName == 'android':
            # 仅支持UiAutomator2
            if action_type == 'accept':
                script = 'mobile:acceptAlert'
            elif action_type == 'dismiss':
                script = 'mobile:dismissAlert'
        elif platformName == 'ios':
            # 仅支持XCUITest
            script = 'mobile:alert'
            script_arg.update({'action': action_type})
        self._driver.execute_script(script, script_arg)

    def is_toast_visible(self, text, platformName='android', automationName='UiAutomator2', isRegexp=False,
                         wait_seconds=5):
        """
        仅支持Android
        :param text:
        :param platformName: android、ios
        :param automationName: 支持UiAutomator2、Espresso
        :param isRegexp: 仅当automaitionName为Espresso时有效
        :return:
        """
        if not text:
            return False
        if 'android' == platformName.lower():
            if 'uiautomator2' == automationName.lower():
                toast_element = CreateElement.create(Locator_Type.XPATH, ".//*[contains(@text,'%s')]" % text, None,
                                                     Wait_By.PRESENCE_OF_ELEMENT_LOCATED, wait_seconds=wait_seconds)
                try:
                    self.getElement(toast_element)
                    return True
                except:
                    return False
            elif 'espresso' == automationName.lower():
                script_arg = {'text': text}
                if isRegexp:
                    script_arg.update({'isRegexp': True})
                script = 'mobile:isToastVisible'
                return self._driver.execute_script(script, script_arg)
        elif 'ios' == platformName.lower():
            return False

    def is_text_exist(self, text: str, wait_seconds: int = 3) -> bool:
        """
        判断text是否于当前页面存在
        """
        try:
            # 使用WebDriverWait等待元素出现
            element = WebDriverWait(self._driver, wait_seconds).until(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text}')]"))
            )
            return True
        except TimeoutException:
            return False

    def move_cursor_to_element(self, target_element_locator, max_attempts=30, timeout=10):
        """
        移动光标到指定元素。依据当前光标对目标元素的位置来计算下一步点击移动的方向，确保光标移动到目标位置。

        :param target_element_locator: 定位目标元素的 locator (如 AppiumBy.ID 或 AppiumBy.XPATH 等)
        :param max_attempts: 最大按键尝试次数，防止无限循环
        :param timeout: 每次按键后的最大等待时间，用于等待页面响应
        :return: True 表示成功移动到目标元素，False 表示未能找到目标元素
        """
        attempts = 0

        while attempts < max_attempts:
            try:
                # 等待目标元素可见
                target_element = WebDriverWait(self._driver, timeout).until(
                    EC.presence_of_element_located(target_element_locator)
                )
                current_element = self._driver.switch_to.active_element
                current_rect = current_element.rect
                target_rect = target_element.rect

                # 获取当前光标和目标元素的中心点坐标
                current_center = {
                    'x': current_rect['x'] + current_rect['width'] / 2,
                    'y': current_rect['y'] + current_rect['height'] / 2
                }
                target_center = {
                    'x': target_rect['x'] + target_rect['width'] / 2,
                    'y': target_rect['y'] + target_rect['height'] / 2
                }

                # 计算水平和垂直方向的差距
                horizontal_diff = target_center['x'] - current_center['x']
                vertical_diff = target_center['y'] - current_center['y']

                # 优先移动差距较大的方向
                if abs(vertical_diff) > abs(horizontal_diff):
                    if vertical_diff > 0:
                        direction = 'down'
                    else:
                        direction = 'up'
                elif abs(horizontal_diff) > 0:
                    if horizontal_diff > 0:
                        direction = 'right'
                    else:
                        direction = 'left'
                else:
                    # 如果差距为 0，说明已经在目标元素上
                    logger.info(f"光标已成功移动到目标元素: {target_element_locator}")
                    return True

                # 按下对应方向的键
                self._press_directional_key(direction)
                attempts += 1

            except TimeoutException:
                logger.warning(f"目标元素未出现，继续尝试... {attempts + 1}/{max_attempts}")
                attempts += 1
            except StaleElementReferenceException:
                logger.warning("元素发生变化，可能已被更新或消失，重新获取当前和目标元素")
            except Exception as e:
                logger.error(f"发生未知错误: {e}")
                break

        logger.warning(f"未能在 {max_attempts} 次尝试中找到目标元素")
        return False

    def _press_directional_key(self, direction):
        """
        模拟方向键按下，支持上下左右方向键。

        :param direction: 'up', 'down', 'left', 'right'
        """
        key_codes = {
            'up': 19,  # Android KeyEvent.KEYCODE_DPAD_UP
            'down': 20,  # Android KeyEvent.KEYCODE_DPAD_DOWN
            'left': 21,  # Android KeyEvent.KEYCODE_DPAD_LEFT
            'right': 22  # Android KeyEvent.KEYCODE_DPAD_RIGHT
        }

        if direction in key_codes:
            logger.info(f"按下方向键: {direction}")
            self._driver.press_keycode(key_codes[direction])
        else:
            logger.error(f"未知的方向键: {direction}")

    def get_geolocation(self):
        """
        返回定位信息,纬度/经度/高度
        :return:
        """
        httpResponseResult = self._doRequest.get('/session/' + self._session_id + '/location')
        return httpResponseResult.body

    def set_geolocation(self, latitude, longitude, altitude):
        """
        设置定位信息
        :param latitude: 纬度 -90 ~ 90
        :param longitude: 精度 ~180 ~ 180
        :param altitude: 高度
        :return:
        """
        geolocation = {}
        location = {}
        location.update({'latitude': latitude})
        location.update({'longitude': longitude})
        location.update({'altitude': altitude})
        geolocation.update({'location': location})
        self._doRequest.post_with_form('/session/' + self._session_id + '/location', params=ujson.dumps(geolocation))

    def start_activity(self, package_name, activity_name):
        """
        启动Android的activity
        """
        self._driver.start_activity(package_name, activity_name)

    def get_current_activity(self):
        """
        获得Android的activity
        :return:
        """
        return self._driver.current_activity

    def get_current_package(self):
        """
        获得Android的package
        :return:
        """
        return self._driver.current_package

    def execute_javascript(self, script):
        """
        仅适用于web
        :param script:
        :return:
        """
        self._driver.execute_script(script)

    def install_app(self, filePath):
        self._driver.install_app(os.path.abspath(filePath))

    def remove_app(self, app_id):
        self._driver.remove_app(app_id)

    def launch_app(self):
        self._driver.launch_app()

    def reset_app(self):
        """
        重置app，可以进入下一轮app测试
        :return:
        """
        return self._driver.reset()

    def close_app(self):
        self._driver.close_app()

    def background_app(self, seconds):
        """
        后台运行
        :param seconds: -1代表完全停用
        :return:
        """
        self._driver.background_app(seconds)

    def activate_app(self, app_id):
        """
        :param app_id: IOS是bundleId，Android是Package名
        """
        self._driver.activate_app(app_id)

    def terminate_app(self, app_id, timeout=None):
        """
        :param app_id IOS是bundleId，Android是Package名
        :param timeout 重试超时时间，仅支持Android
        """
        if timeout:
            self._driver.terminate_app(app_id, timeout=timeout)
        else:
            self._driver.terminate_app(app_id)

    def get_app_state(self, app_id):
        """
        :param app_id IOS是bundleId，Android是Package名
        :return: 0:未安装,1:不在运行,2:在后台运行或者挂起,3:在后台运行,4:在前台运行
        """
        return self._driver.query_app_state(app_id)

    def get_clipboard(self):
        return self._driver.get_clipboard()

    def set_clipboard(self, text):
        self._driver.set_clipboard(text)

    def push_file_to_device(self, device_filePath, local_filePath):
        """
        上传文件设备
        :param device_filePath:
        :param local_filePath:
        :return:
        """
        local_filePath = os.path.abspath(local_filePath)
        with open(local_filePath, 'rb') as f:
            data = base64.b64encode(f.read())
            f.close()
        self._driver.push_file(device_filePath, data)

    def pull_file_from_device(self, device_filePath, local_filePath):
        """
        从设备上下载文件
        :param device_filePath:
        :param local_filePath:
        :return:
        """
        local_filePath = os.path.abspath(local_filePath)
        data = self._driver.pull_file(device_filePath)
        with open(local_filePath, 'wb') as f:
            f.write(base64.b64decode(data))
            f.close()

    def lock_screen(self, seconds=None):
        self._driver.lock(seconds)

    def unlock_screen(self):
        self._driver.unlock()

    def press_keycode(self, keycode):
        """
        按键盘按键，仅支持Android
        :param keycode: 键盘上每个按键的ascii
        :return:
        """
        self._driver.press_keycode(keycode)

    def long_press_keycode(self, keycode):
        """
        长按键盘按键，仅支持Android
        :param keycode:
        :return:
        """
        self._driver.long_press_keycode(keycode)

    def hide_keyboard(self):
        """
        隐藏键盘,Android无需参数
        :return:
        """
        self._driver.hide_keyboard()

    def toggle_airplane_mode(self):
        """
        切换飞行模式(开启关闭),仅支持Android
        :return:
        """
        self._doRequest.post_with_form('/session/' + self._session_id + '/appium/device/toggle_airplane_mode')

    def toggle_data(self):
        """
        切换蜂窝数据模式(开启关闭),仅支持Android
        :return:
        """
        self._doRequest.post_with_form('/session/' + self._session_id + '/appium/device/toggle_data')

    def toggle_wifi(self):
        """
        切换wifi模式(开启关闭),仅支持Android
        :return:
        """
        self._driver.toggle_wifi()

    def toggle_location_services(self):
        """
        切换定位服务模式(开启关闭),仅支持Android
        :return:
        """
        self._driver.toggle_location_services()

    def get_performance_date(self, data_type, package_name=None, data_read_timeout=10):
        """
        获得设备性能数据
        :param package_name:
        :param data_type: cpuinfo、batteryinfo、networkinfo、memoryinfo
        :param data_read_timeout:
        :return:
        """
        if data_type in self._driver.get_performance_data_types():
            return self._driver.get_performance_data(package_name, data_type, data_read_timeout)

    def start_recording_screen(self):
        """
        默认录制为3分钟,android最大只能3分钟,ios最大只能10分钟。如果录制产生的视频文件过大无法放到手机内存里会抛异常，所以尽量录制短视频
        :return:
        """
        self._driver.start_recording_screen(forcedRestart=True)

    def stop_recording_screen(self, fileName=''):
        """
        停止录像并将视频附加到报告里
        :param fileName:
        :return:
        """
        fileName = DateTimeTool.getNowTime('%Y%m%d%H%M%S%f_') + fileName
        data = self._driver.stop_recording_screen()
        allure.attach(name=fileName, body=base64.b64decode(data), attachment_type=allure.attachment_type.MP4)

    def get_device_time(self, format=None):
        """
        获得设备时间
        :param format: eg.YYYY-MM-DD
        :return:
        """
        return self._driver.get_device_time(format)

    def get_element_location(self, element):
        """
        获得元素在屏幕的位置,x、y坐标为元素左上角
        :param element:
        :return:
        """
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            return webElement.location

    def get_element_center_location(self, element):
        """
        获得元素中心的x、y坐标
        :param element:
        :return:
        """
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            rect = webElement.rect
            height = rect['height']
            width = rect['width']
            x = rect['x']
            y = rect['y']
            result_x = x + width / 2
            result_y = y + height / 2
            return {'x': result_x, 'y': result_y}

    def touch_element_left_slide(self, element, start_x_percent=0.5, start_y_percent=0.5, duration=500,
                                 edge_type='element'):
        """
        通过元素宽度、高度的百分比值的位置点击滑动到元素或者屏幕的左边缘
        :param element:
        :param start_x_percent: 相对元素宽度的百分比
        :param start_y_percent: 相对元素高度的百分比
        :param duration:
        :param edge_type: element:滑动到元素边缘,screen:滑动到屏幕边缘
        :return:
        """
        if start_x_percent >= 1:
            start_x_percent = 0.99
        if start_y_percent >= 1:
            start_y_percent = 0.99
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            rect = webElement.rect
            height = rect['height']
            width = rect['width']
            x = rect['x']
            y = rect['y']
            start_x = x + width * start_x_percent
            start_y = y + height * start_y_percent
            if edge_type.lower() == 'element':
                end_x = x + 0.01
                end_y = y + height * 0.5
            elif edge_type.lower() == 'screen':
                end_x = 0 + 0.01
                end_y = self._window_size['height'] * 0.5
            else:
                end_x = start_x
                end_y = end_x
            self._driver.swipe(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y, duration=duration)

    def touch_element_right_slide(self, element, start_x_percent=0.5, start_y_percent=0.5, duration=500,
                                  edge_type='element'):
        """
        通过元素宽度、高度的百分比值的位置点击滑动到元素或者屏幕的右边缘
        :param element:
        :param start_x_percent: 相对元素宽度的百分比
        :param start_y_percent: 相对元素高度的百分比
        :param duration:
        :param edge_type: element:滑动到元素边缘,screen:滑动到屏幕边缘
        :return:
        """
        if start_x_percent >= 1:
            start_x_percent = 0.99
        if start_y_percent >= 1:
            start_y_percent = 0.99
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            rect = webElement.rect
            height = rect['height']
            width = rect['width']
            x = rect['x']
            y = rect['y']
            start_x = x + width * start_x_percent
            start_y = y + height * start_y_percent
            if edge_type.lower() == 'element':
                end_x = x + width * 0.99
                end_y = y + height * 0.5
            elif edge_type.lower() == 'screen':
                end_x = self._window_size['width'] * 0.99
                end_y = self._window_size['height'] * 0.5
            else:
                end_x = start_x
                end_y = end_x
            self._driver.swipe(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y, duration=duration)

    def touch_element_up_slide(self, element, start_x_percent=0.5, start_y_percent=0.5, duration=500,
                               edge_type='element'):
        """
        通过元素宽度、高度的百分比值的位置点击滑动到元素或者屏幕的上边缘
        :param element:
        :param start_x_percent: 相对元素宽度的百分比
        :param start_y_percent: 相对元素高度的百分比
        :param duration:
        :param edge_type: element:滑动到元素边缘,screen:滑动到屏幕边缘
        :return:
        """
        if start_x_percent >= 1:
            start_x_percent = 0.99
        if start_y_percent >= 1:
            start_y_percent = 0.99
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            rect = webElement.rect
            height = rect['height']
            width = rect['width']
            x = rect['x']
            y = rect['y']
            start_x = x + width * start_x_percent
            start_y = y + height * start_y_percent
            if edge_type.lower() == 'element':
                end_x = x + width * 0.5
                end_y = y + 0.01
            elif edge_type.lower() == 'screen':
                end_x = self._window_size['width'] * 0.5
                end_y = 0 + 0.01
            else:
                end_x = start_x
                end_y = end_x
            self._driver.swipe(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y, duration=duration)

    def touch_element_down_slide(self, element, start_x_percent=0.5, start_y_percent=0.5, duration=500,
                                 edge_type='element'):
        """
        通过元素宽度、高度的百分比值的位置点击滑动到元素或者屏幕的下边缘
        :param element:
        :param start_x_percent: 相对元素宽度的百分比
        :param start_y_percent: 相对元素高度的百分比
        :param duration:
        :param edge_type: element:滑动到元素边缘,screen:滑动到屏幕边缘
        :return:
        """
        if start_x_percent >= 1:
            start_x_percent = 0.99
        if start_y_percent >= 1:
            start_y_percent = 0.99
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            rect = webElement.rect
            height = rect['height']
            width = rect['width']
            x = rect['x']
            y = rect['y']
            start_x = x + width * start_x_percent
            start_y = y + height * start_y_percent
            if edge_type.lower() == 'element':
                end_x = x + width * 0.5
                end_y = y + height * 0.99
            elif edge_type.lower() == 'screen':
                end_x = self._window_size['width'] * 0.5
                end_y = self._window_size['height'] * 0.99
            else:
                end_x = start_x
                end_y = end_x
            self._driver.swipe(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y, duration=duration)

    def touch_a_element_to_another_element_slide(self, src_element, dst_element, src_start_x_percent=0.5,
                                                 src_start_y_percent=0.5,
                                                 dst_end_x_percent=0.5, dst_end_y_percent=0.5, duration=500):
        """
        通过一个元素宽度、高度的百分比值的位置点击滑动到另一个元素宽度、高度的百分比值的位置
        :param src_element: 开始的元素
        :param dst_element: 结束的元素
        :param src_start_x_percent: 相对元素宽度的百分比
        :param src_start_y_percent: 相对元素高度的百分比
        :param dst_end_x_percent: 相对元素宽度的百分比
        :param dst_end_y_percent: 相对元素高度的百分比
        :return:
        """
        if src_start_x_percent >= 1:
            src_start_x_percent = 0.99
        if src_start_y_percent >= 1:
            src_start_y_percent = 0.99
        if dst_end_x_percent >= 1:
            dst_end_x_percent = 0.99
        if dst_end_y_percent >= 1:
            dst_end_y_percent = 0.99
        src_webElement = self._change_element_to_webElement_type(src_element)
        dst_webElement = self._change_element_to_webElement_type(dst_element)
        if src_webElement and dst_webElement:
            src_rect = src_webElement.rect
            src_height = src_rect['height']
            src_width = src_rect['width']
            src_x = src_rect['x']
            src_y = src_rect['y']
            dst_rect = dst_webElement.rect
            dst_height = dst_rect['height']
            dst_width = dst_rect['width']
            dst_x = dst_rect['x']
            dst_y = dst_rect['y']
            # 计算位置
            start_x = src_x + src_width * src_start_x_percent
            start_y = src_y + src_height * src_start_y_percent
            end_x = dst_x + dst_width * dst_end_x_percent
            end_y = dst_y + dst_height * dst_end_y_percent
            self._driver.swipe(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y, duration=duration)

    def touch_a_element_move_to_another_element(self, src_element, dst_element, src_start_x_percent=0.5,
                                                src_start_y_percent=0.5,
                                                dst_end_x_percent=0.5, dst_end_y_percent=0.5, long_press=True,
                                                duration=0):
        """
        通过一个元素宽度、高度的百分比值的位置点击移动到另一个元素宽度、高度的百分比值的位置
        :param src_element: 开始的元素
        :param dst_element: 结束的元素
        :param src_start_x_percent: 相对元素宽度的百分比
        :param src_start_y_percent: 相对元素高度的百分比
        :param dst_end_x_percent: 相对元素宽度的百分比
        :param dst_end_y_percent: 相对元素高度的百分比
        :param long_press: 是否长按
        :param duration: 耗时
        :return:
        """
        if src_start_x_percent >= 1:
            src_start_x_percent = 0.99
        if src_start_y_percent >= 1:
            src_start_y_percent = 0.99
        if dst_end_x_percent >= 1:
            dst_end_x_percent = 0.99
        if dst_end_y_percent >= 1:
            dst_end_y_percent = 0.99
        src_webElement = self._change_element_to_webElement_type(src_element)
        dst_webElement = self._change_element_to_webElement_type(dst_element)
        if src_webElement and dst_webElement:
            src_rect = src_webElement.rect
            src_height = src_rect['height']
            src_width = src_rect['width']
            src_x = src_rect['x']
            src_y = src_rect['y']
            dst_rect = dst_webElement.rect
            dst_height = dst_rect['height']
            dst_width = dst_rect['width']
            dst_x = dst_rect['x']
            dst_y = dst_rect['y']
            # 计算位置
            start_x = src_x + src_width * src_start_x_percent
            start_y = src_y + src_height * src_start_y_percent
            end_x = dst_x + dst_width * dst_end_x_percent
            end_y = dst_y + dst_height * dst_end_y_percent
            self.touch_move_to(start_x, start_y, end_x, end_y, long_press, duration)

    def get_element_size_in_pixels(self, element):
        """
        返回元素的像素大小
        :param element:
        :return:
        """
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            return webElement.size

    def get_all_contexts(self):
        """
        获得能够自动化测所有上下文(混合应用中的原生应用和web应用)
        :return:
        """
        return self._driver.contexts

    def get_current_context(self):
        """
        获得当前appium中正在运行的上下文(混合应用中的原生应用和web应用)
        :return:
        """
        return self._driver.current_context

    def switch_context(self, context_name):
        """
        切换上下文(混合应用中的原生应用和web应用)
        :param context_name:
        :return:
        """
        context = {}
        context.update({'name': context_name})
        self._doRequest.post_with_form('/session/' + self._session_id + '/context', params=ujson.dumps(context))

    def touch_move_to(self, start_x, start_y, end_x, end_y, long_press=True, duration=0):
        """
        点击从一个点移动到另外一个点
        :param start_x:
        :param start_y:
        :param end_x:
        :param end_y:
        :param long_press: 是否长按
        :param duration: 为0时不会出现惯性滑动
        :return:
        """
        if long_press:
            action = TouchAction(self._driver)
            action.long_press(x=start_x, y=start_y, duration=duration).move_to(x=end_x, y=end_y).release().perform()
        else:
            actions = TouchAction(self._driver)
            actions.press(x=start_x, y=start_y).wait(duration)
            actions.move_to(x=end_x, y=end_y)
            actions.perform()

    def tap(self, x: float, y: float, duration=None):
        """点击坐标

        Args:
            x (float): 
            y (float): 
            duration ([type], optional): [description]. Defaults to None.
        """
        self._driver.tap([(x, y)], duration)

    def touch_tap(self, element, xoffset=None, yoffset=None, count=1, is_perfrom=True):
        """
        触屏点击
        1、如果xoffset和yoffset都None,则在指定元素的正中间进行点击
        2、如果element、xoffset和yoffset都不为None,则根据元素的左上角做x和y的偏移然后进行点击
        :param element:
        :param xoffset:
        :param yoffset:
        :param count: 点击次数
        :param is_perfrom 是否马上执行动作,不执行可以返回动作给多点触控执行
        :return:
        """
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            actions = TouchAction(self._driver)
            actions.tap(webElement, xoffset, yoffset, count)
            if is_perfrom:
                actions.perform()
            return actions

    def touch_long_press(self, element, xoffset=None, yoffset=None, duration_sconds=10, is_perfrom=True):
        """
        触屏长按
        1、如果xoffset和yoffset都None,则在指定元素的正中间进行长按
        2、如果element、xoffset和yoffset都不为None,则根据元素的左上角做x和y的偏移然后进行长按
        :param element:
        :param xoffset:
        :param yoffset:
        :param duration_sconds: 长按秒数
        :param is_perfrom 是否马上执行动作,不执行可以返回动作给多点触控执行
        :return:
        """
        webElement = self._change_element_to_webElement_type(element)
        if webElement:
            actions = TouchAction(self._driver)
            actions.long_press(webElement, xoffset, yoffset, duration_sconds * 1000)
            if is_perfrom:
                actions.perform()
            return actions

    def multi_touch_actions_perform(self, touch_actions):
        """
        多点触控执行
        :param touch_actions:
        :return:
        """
        multiActions = MultiAction(self._driver)
        for actions in touch_actions:
            multiActions.add(actions)
        multiActions.perform()

    def touch_slide(self, start_element=None, start_x=None, start_y=None, end_element=None, end_x=None, end_y=None,
                    duration=None):
        """
        滑动屏幕,在指定时间内从一个位置滑动到另外一个位置
        1、如果start_element不为None,则从元素的中间位置开始滑动
        2、如果end_element不为None,滑动结束到元素的中间位置
        :param start_element:
        :param end_element:
        :param start_x:
        :param start_y:
        :param end_x:
        :param end_y:
        :param duration: 毫秒
        :return:
        """
        start_webElement = self._change_element_to_webElement_type(start_element)
        end_webElement = self._change_element_to_webElement_type(end_element)
        if start_webElement:
            start_webElement_location = self.get_element_location(start_webElement)
            start_x = start_webElement_location['x']
            start_y = start_webElement_location['y']
        if end_webElement:
            end_webElement_location = self.get_element_location(end_webElement)
            end_x = end_webElement_location['x']
            end_y = end_webElement_location['y']
        self._driver.swipe(start_x, start_y, end_x, end_y, duration)

    def touch_left_slide(self, start_x_percent=0.5, start_y_percent=0.5, duration=500):
        """
        通过屏幕宽度、高度的百分比值的位置点击滑动到元素的左边缘
        :param start_x_percent: 相对屏幕宽度的百分比
        :param start_y_percent: 相对屏幕高度的百分比
        :return:
        """
        if start_x_percent >= 1:
            start_x_percent = 0.99
        if start_y_percent >= 1:
            start_y_percent = 0.99
        start_x = self._window_size['width'] * start_x_percent
        start_y = self._window_size['height'] * start_y_percent
        end_x = 0
        end_y = self._window_size['height'] * 0.5
        self._driver.swipe(start_x, start_y, end_x, end_y, duration)

    def touch_right_slide(self, start_x_percent=0.5, start_y_percent=0.5, duration=500):
        """
        通过屏幕宽度、高度的百分比值的位置点击滑动到元素的右边缘
        :param start_x_percent: 相对屏幕宽度的百分比
        :param start_y_percent: 相对屏幕高度的百分比
        :return:
        """
        if start_x_percent >= 1:
            start_x_percent = 0.99
        if start_y_percent >= 1:
            start_y_percent = 0.99
        start_x = self._window_size['width'] * start_x_percent
        start_y = self._window_size['height'] * start_y_percent
        end_x = self._window_size['width'] * 0.99
        end_y = self._window_size['height'] * 0.5
        self._driver.swipe(start_x, start_y, end_x, end_y, duration)

    def touch_up_slide(self, start_x_percent=0.5, start_y_percent=0.5, duration=500):
        """
        通过屏幕宽度、高度的百分比值的位置点击滑动到元素的上边缘
        :param start_x_percent: 相对屏幕宽度的百分比
        :param start_y_percent: 相对屏幕高度的百分比
        :return:
        :return:
        """
        if start_x_percent >= 1:
            start_x_percent = 0.99
        if start_y_percent >= 1:
            start_y_percent = 0.99
        start_x = self._window_size['width'] * start_x_percent
        start_y = self._window_size['height'] * start_y_percent
        end_x = self._window_size['width'] * 0.5
        end_y = 0
        self._driver.swipe(start_x, start_y, end_x, end_y, duration)

    def touch_down_slide(self, start_x_percent=0.5, start_y_percent=0.5, duration=500):
        """
        通过屏幕宽度、高度的百分比值的位置点击滑动到元素的下边缘
        :param start_x_percent: 相对屏幕宽度的百分比
        :param start_y_percent: 相对屏幕高度的百分比
        :return:
        :return:
        """
        if start_x_percent >= 1:
            start_x_percent = 0.99
        if start_y_percent >= 1:
            start_y_percent = 0.99
        start_x = self._window_size['width'] * start_x_percent
        start_y = self._window_size['height'] * start_y_percent
        end_x = self._window_size['width'] * 0.5
        end_y = self._window_size['height'] * 0.99
        self._driver.swipe(start_x, start_y, end_x, end_y, duration)

    def getElement(self, elementInfo):
        """
        定位单个元素
        :param elementInfo:
        :return:
        """
        webElement = None
        locator_type = elementInfo.locator_type
        locator_value = elementInfo.locator_value
        wait_type = elementInfo.wait_type
        wait_seconds = elementInfo.wait_seconds
        wait_expected_value = elementInfo.wait_expected_value
        if wait_expected_value:
            wait_expected_value = wait_expected_value

        # 查找元素,为了保证元素被定位,都进行显式等待
        if wait_type == Wait_By.TITLE_IS:
            webElement = WebDriverWait(self._driver, wait_seconds).until(
                expected_conditions.title_is(wait_expected_value))
        elif wait_type == Wait_By.TITLE_CONTAINS:
            webElement = WebDriverWait(self._driver, wait_seconds).until(
                expected_conditions.title_contains(wait_expected_value))
        elif wait_type == Wait_By.PRESENCE_OF_ELEMENT_LOCATED:
            webElement = WebDriverWait(self._driver, wait_seconds).until(
                expected_conditions.presence_of_element_located((locator_type, locator_value)))
        elif wait_type == Wait_By.ELEMENT_TO_BE_CLICKABLE:
            webElement = WebDriverWait(self._driver, wait_seconds).until(
                expected_conditions.element_to_be_clickable((locator_type, locator_value)))
        elif wait_type == Wait_By.ELEMENT_LOCATED_TO_BE_SELECTED:
            webElement = WebDriverWait(self._driver, wait_seconds).until(
                expected_conditions.element_located_to_be_selected((locator_type, locator_value)))
        elif wait_type == Wait_By.VISIBILITY_OF:
            webElements = WebDriverWait(self._driver, wait_seconds).until(
                (expected_conditions.visibility_of_all_elements_located((locator_type, locator_value))))
            if len(webElements) > 0:
                webElement = webElements[0]
        else:
            if locator_type == By.ID:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element_by_id(locator_value))
            elif locator_type == By.NAME:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element_by_name(locator_value))
            elif locator_type == By.LINK_TEXT:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element_by_link_text(locator_value))
            elif locator_type == By.XPATH:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element_by_xpath(locator_value))
            elif locator_type == By.PARTIAL_LINK_TEXT:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element_by_partial_link_text(locator_value))
            elif locator_type == By.CSS_SELECTOR:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element_by_css_selector(locator_value))
            elif locator_type == By.CLASS_NAME:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element_by_class_name(locator_value))
            elif locator_type == By.TAG_NAME:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element_by_tag_name(locator_value))
            elif locator_type == Locator_Type.ACCESSIBILITY_ID:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element_by_accessibility_id(locator_value))
            elif locator_type == Locator_Type.IMAGE:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element_by_image(locator_value))
            elif locator_type == Locator_Type.ANDROID_UIAUTOMATOR:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element_by_android_uiautomator(locator_value))
            elif locator_type == Locator_Type.ANDROID_DATA_MATCHER:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element_by_android_data_matcher(locator_value))
            elif locator_type == Locator_Type.ANDROID_VIEWTAG:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element_by_android_viewtag(locator_value))
            elif locator_type == Locator_Type.IOS_UIAUTOMATION:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element_by_ios_uiautomation(locator_value))
            elif locator_type == Locator_Type.IOS_CLASS_CHAIN:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element_by_ios_class_chain(locator_value))
            elif locator_type == Locator_Type.IOS_PREDICATE:
                webElement = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_element_by_ios_predicate(locator_value))
        return webElement

    def getElements(self, elementInfo):
        """
        定位多个元素
        :param elementInfo:
        :return:
        """
        webElements = None
        locator_type = elementInfo.locator_type
        locator_value = elementInfo.locator_value
        wait_type = elementInfo.wait_type
        wait_seconds = elementInfo.wait_seconds

        # 查找元素,为了保证元素被定位,都进行显式等待
        if wait_type == Wait_By.PRESENCE_OF_ELEMENT_LOCATED:
            webElements = WebDriverWait(self._driver, wait_seconds).until(
                expected_conditions.presence_of_all_elements_located((locator_type, locator_value)))
        elif wait_type == Wait_By.VISIBILITY_OF:
            webElements = WebDriverWait(self._driver, wait_seconds).until(
                expected_conditions.visibility_of_all_elements_located((locator_type, locator_value)))
        else:
            if locator_type == By.ID:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements_by_id(locator_value))
            elif locator_type == By.NAME:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements_by_name(locator_value))
            elif locator_type == By.LINK_TEXT:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements_by_link_text(locator_value))
            elif locator_type == By.XPATH:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements_by_xpath(locator_value))
            elif locator_type == By.PARTIAL_LINK_TEXT:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements_by_partial_link_text(locator_value))
            elif locator_type == By.CSS_SELECTOR:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements_by_css_selector(locator_value))
            elif locator_type == By.CLASS_NAME:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements_by_class_name(locator_value))
            elif locator_type == By.TAG_NAME:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements_by_tag_name(locator_value))
            elif locator_type == Locator_Type.ACCESSIBILITY_ID:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements_by_accessibility_id(locator_value))
            elif locator_type == Locator_Type.IMAGE:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements_by_image(locator_value))
            elif locator_type == Locator_Type.ANDROID_UIAUTOMATOR:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements_by_android_uiautomator(locator_value))
            elif locator_type == Locator_Type.ANDROID_DATA_MATCHER:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements_by_android_data_matcher(locator_value))
            elif locator_type == Locator_Type.ANDROID_VIEWTAG:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements_by_android_viewtag(locator_value))
            elif locator_type == Locator_Type.IOS_UIAUTOMATION:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements_by_ios_uiautomation(locator_value))
            elif locator_type == Locator_Type.IOS_CLASS_CHAIN:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements_by_ios_class_chain(locator_value))
            elif locator_type == Locator_Type.IOS_PREDICATE:
                webElements = WebDriverWait(self._driver, wait_seconds).until(
                    lambda driver: driver.find_elements_by_ios_predicate(locator_value))
        return webElements

    def getSubElement(self, parent_element, sub_elementInfo):
        """
        获得元素的单个子元素
        :param parent_element: 父元素
        :param sub_elementInfo: 子元素,只能提供pojo.elementInfo.ElementInfo类型
        :return:
        """
        webElement = self._change_element_to_webElement_type(parent_element)
        if not webElement:
            return None
        if not isinstance(sub_elementInfo, ElementInfo):
            return None

        # 通过父元素查找子元素
        locator_type = sub_elementInfo.locator_type
        locator_value = sub_elementInfo.locator_value
        wait_seconds = sub_elementInfo.wait_seconds

        # 查找元素,为了保证元素被定位,都进行显式等待
        if locator_type == By.ID:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element_by_id(locator_value))
        elif locator_type == By.NAME:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element_by_name(locator_value))
        elif locator_type == By.LINK_TEXT:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element_by_link_text(locator_value))
        elif locator_type == By.XPATH:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element_by_xpath(locator_value))
        elif locator_type == By.PARTIAL_LINK_TEXT:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element_by_partial_link_text(locator_value))
        elif locator_type == By.CSS_SELECTOR:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element_by_css_selector(locator_value))
        elif locator_type == By.CLASS_NAME:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element_by_class_name(locator_value))
        elif locator_type == By.TAG_NAME:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element_by_tag_name(locator_value))
        elif locator_type == Locator_Type.ACCESSIBILITY_ID:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element_by_accessibility_id(locator_value))
        elif locator_type == Locator_Type.IMAGE:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element_by_image(locator_value))
        elif locator_type == Locator_Type.ANDROID_UIAUTOMATOR:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element_by_android_uiautomator(locator_value))
        elif locator_type == Locator_Type.ANDROID_DATA_MATCHER:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element_by_android_data_matcher(locator_value))
        elif locator_type == Locator_Type.ANDROID_VIEWTAG:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element_by_android_viewtag(locator_value))
        elif locator_type == Locator_Type.IOS_UIAUTOMATION:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element_by_ios_uiautomation(locator_value))
        elif locator_type == Locator_Type.IOS_CLASS_CHAIN:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element_by_ios_class_chain(locator_value))
        elif locator_type == Locator_Type.IOS_PREDICATE:
            subWebElement = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_element_by_ios_predicate(locator_value))
        else:
            return None
        return subWebElement

    def getSubElements(self, parent_element, sub_elementInfo):
        """
        获得元素的多个子元素
        :param parent_element: 父元素
        :param sub_elementInfo: 子元素,只能提供pojo.elementInfo.ElementInfo类型
        :return:
        """
        webElement = self._change_element_to_webElement_type(parent_element)
        if not webElement:
            return None
        if not isinstance(sub_elementInfo, ElementInfo):
            return None

        # 通过父元素查找多个子元素
        locator_type = sub_elementInfo.locator_type
        locator_value = sub_elementInfo.locator_value
        wait_seconds = sub_elementInfo.wait_seconds

        # 查找元素,为了保证元素被定位,都进行显式等待
        if locator_type == By.ID:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements_by_id(locator_value))
        elif locator_type == By.NAME:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements_by_name(locator_value))
        elif locator_type == By.LINK_TEXT:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements_by_link_text(locator_value))
        elif locator_type == By.XPATH:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements_by_xpath(locator_value))
        elif locator_type == By.PARTIAL_LINK_TEXT:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements_by_partial_link_text(locator_value))
        elif locator_type == By.CSS_SELECTOR:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements_by_css_selector(locator_value))
        elif locator_type == By.CLASS_NAME:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements_by_class_name(locator_value))
        elif locator_type == By.TAG_NAME:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements_by_tag_name(locator_value))
        elif locator_type == Locator_Type.ACCESSIBILITY_ID:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements_by_accessibility_id(locator_value))
        elif locator_type == Locator_Type.IMAGE:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements_by_image(locator_type))
        elif locator_type == Locator_Type.ANDROID_UIAUTOMATOR:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements_by_android_uiautomator(locator_value))
        elif locator_type == Locator_Type.ANDROID_DATA_MATCHER:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements_by_android_data_matcher(locator_value))
        elif locator_type == Locator_Type.ANDROID_VIEWTAG:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements_by_android_viewtag(locator_value))
        elif locator_type == Locator_Type.IOS_UIAUTOMATION:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements_by_ios_uiautomation(locator_value))
        elif locator_type == Locator_Type.IOS_CLASS_CHAIN:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements_by_ios_class_chain(locator_value))
        elif locator_type == Locator_Type.IOS_PREDICATE:
            subWebElements = WebDriverWait(webElement, wait_seconds).until(
                lambda webElement: webElement.find_elements_by_ios_predicate(locator_value))
        else:
            return None
        return subWebElements

    def getDriver(self):
        return self._driver
