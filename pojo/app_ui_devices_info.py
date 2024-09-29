from base.read_httpserver_config import Read_Http_Server_Config
import os
import logging

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class APP_UI_Devices_Info:
    def __init__(self):
        self.devices_desc = []
        self.app_ui_configs = []
        self.api_configs = []
        self.server_ports = []
        self.server_ips = []
        self.system_auth_alert_labels = []
        self.is_enable_system_auth_check = []
        self.udids = []
        self.platformNames = []
        self.automationNames = []
        self.platformVersions = []
        self.deviceNames = []
        self.chromeDriverPorts = []
        self.chromeDriverPaths = []
        self.recreateChromeDriverSessions = []
        self.nativeWebScreenshots = []
        self.systemports = []
        self.wdaLocalPorts = []
        self.appPackages = []
        self.appActivitys = []
        self.bundleIds = []
        self.apps_dirs = []
        self.apps_urls = []
        self.noSigns = []
        self.fullResets = []
        self.noResets = []

    def get_devices_info(self):
        """
        获取设备信息并构建设备信息字典。

        1. 初始化设备信息列表。
        2. 读取本地IP和端口配置。
        3. 遍历设备描述，构建每个设备的信息字典。
        4. 根据不同条件构建desired_capabilities。
        5. 将设备信息添加到列表中。
        6. 返回设备信息列表。
        """
        devices_info = []

        # 读取HTTP服务器配置
        local_ip = Read_Http_Server_Config().httpserver_config.local_ip
        httpserver_port = Read_Http_Server_Config().httpserver_config.httpserver_port
        logging.info(f"Local IP: {local_ip}, HTTP Server Port: {httpserver_port}")

        # 遍历设备描述
        for i in range(len(self.devices_desc)):
            device_info = {}

            # 更新基本设备信息
            device_info.update({'device_desc': self.devices_desc[i].strip()})
            device_info.update({'app_ui_config': self.app_ui_configs[i].strip()})
            logging.info(f"Processing device {i}: {self.devices_desc[i]}")

            # 如果存在API配置，则更新
            if self.api_configs:
                device_info.update({'api_config': self.api_configs[i]})
                logging.info(f"Adding API config for device {i}: {self.api_configs[i]}")

            # 更新其他设备信息
            device_info.update({'server_port': self.server_ports[i].strip()})
            device_info.update({'server_ip': self.server_ips[i].strip()})
            logging.info(f"Updating server info for device {i}: {self.server_ports[i]}, {self.server_ips[i]}")

            # 如果存在系统认证标签，则更新
            if self.system_auth_alert_labels:
                device_info.update({'system_auth_alert_label': self.system_auth_alert_labels[i]})
                logging.info(f"Adding system auth alert label for device {i}: {self.system_auth_alert_labels[i]}")

            # 更新是否启用系统认证检查
            device_info.update({'is_enable_system_auth_check': self.is_enable_system_auth_check[i]})
            logging.info(f"Enabling system auth check for device {i}: {self.is_enable_system_auth_check[i]}")

            # 构建desired_capabilities
            a_device_capabilities_num = 0
            a_device_appActivitys = []
            a_device_appPackages = []
            a_device_bundleIds = []
            a_device_apps = []

            # 处理appActivity和appPackages
            if len(self.appActivitys) and len(self.appPackages):
                a_device_appActivitys = self.appActivitys[i].split('&&')
                a_device_appPackages = self.appPackages[i].split('&&')
                a_device_capabilities_num = len(a_device_appActivitys)
                logging.info(f"Found appActivity and appPackages for device {i}: {len(a_device_appActivitys)}")

            # 处理bundleIds
            if len(self.bundleIds):
                a_device_bundleIds = self.bundleIds[i].split('&&')
                a_device_capabilities_num = len(a_device_bundleIds)
                logging.info(f"Found bundleIds for device {i}: {len(a_device_bundleIds)}")

            # 处理apps_dirs
            if len(self.apps_dirs):
                try:
                    paths = os.walk(self.apps_dirs[i].strip())
                    for dirPath, dirName, fileNames in paths:
                        for fileName in fileNames:
                            app_url = f'http://{local_ip}:{httpserver_port}/{self.apps_dirs[i].strip()}/{fileName}'
                            a_device_apps.append(app_url)
                            logging.info(f"Appending app URL: {app_url}")
                    a_device_capabilities_num = len(a_device_apps)
                    logging.info(f"Found apps in directory for device {i}: {a_device_capabilities_num}")
                except Exception as e:
                    logging.error(f"Error while processing apps_dirs: {e}")

            # 处理apps_urls
            if len(self.apps_urls):
                a_device_apps = self.apps_urls[i].split('&&')
                a_device_capabilities_num = len(a_device_apps)
                logging.info(f"Found apps_urls for device {i}: {len(a_device_apps)}")

            # 构建desired_capabilities列表
            a_devices_desired_capabilities = []
            for j in range(a_device_capabilities_num):
                desired_capabilities = {}
                desired_capabilities.update({'udid': self.udids[i].strip()})
                desired_capabilities.update({'platformName': self.platformNames[i].strip()})
                logging.info(f"Setting udid and platformName for device {i}: {self.udids[i]}, {self.platformNames[i]}")

                # 如果存在automationNames，则更新
                if len(self.automationNames):
                    desired_capabilities.update({'automationName': self.automationNames[i].strip()})
                    logging.info(f"Setting automationName for device {i}: {self.automationNames[i]}")

                desired_capabilities.update({'platformVersion': self.platformVersions[i].strip()})
                logging.info(f"Setting platformVersion for device {i}: {self.platformVersions[i]}")

                # 如果存在deviceNames，则更新
                if len(self.deviceNames):
                    desired_capabilities.update({'deviceName': self.deviceNames[i].strip()})
                    logging.info(f"Setting deviceName for device {i}: {self.deviceNames[i]}")

                desired_capabilities.update({'systemport': self.systemports[i].strip()})
                logging.info(f"Setting systemport for device {i}: {self.systemports[i]}")

                # 更新appActivity和appPackage
                if len(self.appActivitys) and len(self.appPackages):
                    desired_capabilities.update({'appActivity': a_device_appActivitys[j].strip()})
                    desired_capabilities.update({'appPackage': a_device_appPackages[j].strip()})
                    logging.info(
                        f"Setting appActivity and appPackage for device {i}: {a_device_appActivitys[j]}, {a_device_appPackages[j]}")

                # 更新bundleId
                if len(self.bundleIds):
                    desired_capabilities.update({'bundleId': a_device_bundleIds[j].strip()})
                    logging.info(f"Setting bundleId for device {i}: {a_device_bundleIds[j]}")

                # 更新app
                if len(self.apps_dirs) or len(self.apps_urls):
                    desired_capabilities.update({'app': a_device_apps[j].strip()})
                    logging.info(f"Setting app for device {i}: {a_device_apps[j]}")

                # 更新noSign
                if len(self.noSigns):
                    noSign = 'true' == self.noSigns[i].strip().lower()
                    desired_capabilities.update({'noSign': noSign})
                    logging.info(f"Setting noSign for device {i}: {noSign}")

                # 更新fullReset
                if len(self.fullResets):
                    fullReset = 'true' == self.fullResets[i].strip().lower()
                    desired_capabilities.update({'fullReset': fullReset})
                    logging.info(f"Setting fullReset for device {i}: {fullReset}")

                # 更新noReset
                if len(self.noResets):
                    noReset = 'true' == self.noResets[i].strip().lower()
                    desired_capabilities.update({'noReset': noReset})
                    logging.info(f"Setting noReset for device {i}: {noReset}")

                a_devices_desired_capabilities.append(desired_capabilities)

            # 更新设备信息中的capabilities
            device_info.update({'capabilities': a_devices_desired_capabilities})
            devices_info.append(device_info)
            logging.info(f"Device {i} capabilities added: {len(a_devices_desired_capabilities)}")

        # 返回设备信息列表
        logging.info(f"All devices processed: {devices_info}")
        return devices_info
        # if len(self.chromeDriverPorts):
        #     desired_capabilities.update({'chromedriverPort': self.chromeDriverPorts[i].strip()})
        # if len(self.chromeDriverPaths):
        #     desired_capabilities.update({'chromedriverExecutable': self.chromeDriverPaths[i].strip()})
        # if len(self.recreateChromeDriverSessions):
        #     recreateChromeDriverSessions_value = False
        #     if 'true' == self.recreateChromeDriverSessions[i].strip().lower():
        #         recreateChromeDriverSessions_value = True
        #     desired_capabilities.update({'recreateChromeDriverSessions': recreateChromeDriverSessions_value})
        # if len(self.nativeWebScreenshots):
        #     nativeWebScreenshot = False
        #     if 'true' == self.nativeWebScreenshots[i].strip().lower():
        #         nativeWebScreenshot = True
        #     desired_capabilities.update({'nativeWebScreenshot': nativeWebScreenshot})
        # if len(self.wdaLocalPorts):
        #     desired_capabilities.update({'wdaLocalPort': self.wdaLocalPorts[i].strip()})
