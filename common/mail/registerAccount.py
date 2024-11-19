#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :
 @time        :  2024/11/18 10:45
"""
import json
import time
import websocket
import re
from threading import Timer, Lock
from common.logger.logTool import logger
from common.yamlTool import YamlTool


class WebSocketClient:
    URL = "wss://mail.ipwangxin.cn/ws/email"  # 固定 URL

    def __init__(self):
        self.ws = None
        self.time = 20
        self.account = None
        self.keep_alive_timer = None
        self.keep_alive_running = False
        self.keep_alive_count = 0  # 用于计数保活请求次数
        self.main_thread_timer = None  # 主线程定时器
        self.lock = Lock()  # 线程锁
        self.found_verification_code = False  # 用于标识是否找到验证码
        self.verification_code = None  # 验证码存储
        self.yaml_tool = YamlTool("common/mail/mail.yaml")

    def on_open(self, ws):
        logger.info("WebSocket 连接已打开")
        self.send_message(json.dumps({"event": "DOMAIN_NAME"}))  # 第一次发送默认数据请求

    def _process_emails(self, emails):
        """处理邮件并提取验证码"""
        found_code = False
        for email in emails:
            content = email.get("content")
            if content:
                code = self.extract_verification_code(content)
                if code:
                    logger.info(f"找到验证码: {code}")
                    self.verification_code = code
                    found_code = True
                    self.found_verification_code = True  # 设置为已找到验证码
                    self.stop_keep_alive()  # 停止保活
                    self.ws.close()  # 关闭WebSocket连接
                    break

        if not found_code:
            logger.info("未找到验证码，继续保活")
            self.start_keep_alive()  # 继续保活

    def extract_verification_code(self, content):
        """从邮件内容中提取验证码"""
        match = re.search(r"verification code:\s*<strong>(\d+)</strong>", content)
        return match.group(1) if match else None

    def on_error(self, ws, error):
        logger.error(f"WebSocket 错误: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logger.info(f"WebSocket 连接已关闭，状态码: {close_status_code}, 消息: {close_msg}")

    def send_message(self, message):
        logger.info(f"发送消息: {message}")
        with self.lock:
            self.ws.send(message)

    def on_new_account_message(self, ws, message):
        logger.info(f"收到消息: {message}")
        data = json.loads(message)

        if data.get("event") == "DOMAIN_NAME":
            logger.info(f"域名获取成功: {data.get('data')}")
            """刷新账户并获取新的账户"""
            self.send_message(json.dumps({"event": "REFRESH"}))  # 第二次发送注册数据
        elif data.get("event") == "REFRESH":
            new_account = data.get("data")
            self.yaml_tool.update_nested_value("userRegisterInfoPro", "account", new_account + '@ipwangxin.cn')
            logger.info(f"注册成功，新邮件名：{new_account}")
            """执行获取邮件列表请求"""
            self.send_message(json.dumps({"event": "LIST_MAIL"}))

        elif data.get("event") == "LIST_MAIL":
            logger.info("邮件列表获取成功，解析邮件内容")
            emails = data.get("data", [])
            if not emails:
                logger.info("邮件列表为空，发送保活请求")
                self.start_keep_alive()  # 继续保活
            else:
                self._process_emails(emails)  # 调用处理邮件的方法

        elif data.get("event") == "NEW_EMAIL":
            logger.info("收到新邮件")
            email_data = data.get("data")
            content = email_data.get("content")
            if content:
                code = self.extract_verification_code(content)
                if code:
                    logger.info(f"收到验证码: {code}")
                    self.yaml_tool.update_nested_value("userRegisterInfoPro", "verifyCode", code)
                    self.verification_code = code
                    self.found_verification_code = True
                    self.stop_keep_alive()
                    self.ws.close()  # 关闭WebSocket连接

    def start_with_new_account(self):
        """使用新账户启动"""
        self.ws = websocket.WebSocketApp(self.URL,
                                         on_open=self.on_open,
                                         on_message=self.on_new_account_message,  # 处理新账户的消息
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        # 启动主线程定时器，2分钟后调用 stop_main_thread 方法
        self.main_thread_timer = Timer(self.time, self.stop_main_thread)
        self.main_thread_timer.start()
        self.ws.run_forever()

    def start_keep_alive(self):
        """开始保活，每6秒发送一次请求，持续2分钟"""
        self.keep_alive_running = True
        self.keep_alive_timer = Timer(6, self._start_keep_alive_loop)
        self.keep_alive_timer.start()

    def _start_keep_alive_loop(self):
        """内部方法，启动保活循环"""
        self.keep_alive_loop()
        if self.keep_alive_running and not self.found_verification_code:
            self.start_keep_alive()

    def keep_alive_loop(self):
        """保活循环，每10秒发送一次，持续2分钟"""
        end_time = time.time() + self.time  # 保持2分钟
        while time.time() < end_time and self.keep_alive_running:
            if self.found_verification_code:  # 如果找到验证码，退出循环
                logger.info("找到验证码，退出保活进程")
                self.stop_keep_alive()
                break

            self.keep_alive_count += 1
            if self.keep_alive_count == 3:
                # 每发送三次保活请求后，发送一次 LIST_MAIL 请求
                self.send_message(json.dumps({"event": "LIST_MAIL"}))
                self.keep_alive_count = 0  # 重置保活计数
                self.stop_keep_alive()  # 关闭当前保活线程
                break  # 退出循环
            else:
                # 否则发送 bt 保活请求
                self.send_message(json.dumps({"bt": "bt"}))
            time.sleep(6)

        # 确保2分钟后停止保活
        if time.time() >= end_time:
            self.stop_keep_alive()

    def stop_keep_alive(self):
        """停止保活"""
        self.keep_alive_running = False
        if self.keep_alive_timer:
            self.keep_alive_timer.cancel()
            logger.info("stop keep alive")

    def get_verification_code(self):
        """获取验证码供外部调用"""
        return self.verification_code

    def stop_main_thread(self):
        """停止主线程请求"""
        self.stop_keep_alive()  # 停止保活
        if self.ws:
            self.ws.close()  # 关闭WebSocket连接
        if self.main_thread_timer:
            self.main_thread_timer.cancel()  # 取消主线程定时器
        logger.info("请求已停止")


# 调用示例
if __name__ == "__main__":
    client = WebSocketClient()
    client.start_with_new_account()

    verification_code = client.get_verification_code()
    print(f"获取到的验证码: {verification_code}")
