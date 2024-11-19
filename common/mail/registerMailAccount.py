#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      : Frankie
 @description : WebSocket 客户端，用于处理邮件验证码提取
 @time        : 2024/11/18 10:45
"""
import json
import websocket
import re
from threading import Timer, Lock
from datetime import datetime, timedelta
from common.logger.logTool import logger
from common.yamlTool import YamlTool


class WebSocketClient:
    URL = "wss://mail.ipwangxin.cn/ws/email"  # 固定 URL
    KEEP_ALIVE_INTERVAL = 6  # 保活间隔时间（秒）
    TIME_LIMIT = 120  # 主线程超时时间（秒）
    MAX_KEEP_ALIVE_ATTEMPTS = 3  # 最大保活次数

    def __init__(self):
        self.ws = None
        self.account = None
        self.keep_alive_timer = None
        self.keep_alive_running = False
        self.keep_alive_attempts = 0
        self.main_thread_timer = None
        self.found_verification_code = False
        self.lock = Lock()
        self.verification_code = None

    # ========== WebSocket 回调方法 ==========
    def on_open(self, ws):
        logger.info("WebSocket 连接已打开")
        self.send_message({"event": "DOMAIN_NAME"})

    def on_message(self, ws, message):
        logger.info(f"收到消息: {message}")
        try:
            data = json.loads(message)
            event = data.get("event")
            event_handlers = {
                "DOMAIN_NAME": self.handle_domain_name,
                "REFRESH": self.handle_refresh,
                "LIST_MAIL": self.handle_list_mail,
                "NEW_EMAIL": self.handle_new_email,
            }
            if event in event_handlers:
                event_handlers[event](data)
            else:
                logger.warning(f"未处理的事件: {event}")
        except json.JSONDecodeError:
            logger.error("解析消息时发生错误")

    def on_error(self, ws, error):
        logger.error(f"WebSocket 错误: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logger.info(f"WebSocket 连接已关闭，状态码: {close_status_code}, 消息: {close_msg}")

    # ========== 消息处理方法 ==========
    def handle_domain_name(self, data):
        logger.info(f"域名获取成功: {data.get('data')}")
        self.send_message({"event": "REFRESH"})

    def handle_refresh(self, data):
        account = data.get("data")
        if account:
            self.account = f"{account}@ipwangxin.cn"
            YamlTool("common/mail/mail.yaml").update_nested_value("userRegisterInfoPro", "account", self.account)
            logger.info(f"注册成功，新账户: {self.account}")
            self.send_message({"event": "LIST_MAIL"})

    def handle_list_mail(self, data):
        emails = data.get("data", [])
        if emails:
            self.process_emails(emails)
        else:
            logger.info("邮件列表为空，启动保活")
            self.start_keep_alive()

    def handle_new_email(self, data):
        email = data.get("data", {})
        content = email.get("content")
        if content:
            self.extract_and_save_verification_code(content)

    # ========== 邮件处理方法 ==========
    def process_emails(self, emails):
        """处理邮件列表并提取两分钟内的最新验证码"""
        current_time = datetime.now()
        two_minutes_ago = current_time - timedelta(minutes=2)

        # 筛选两分钟内的邮件并按接收时间排序
        valid_emails = [
            email for email in emails
            if "receivedTime" in email and datetime.fromtimestamp(email["receivedTime"] / 1000) > two_minutes_ago
        ]
        valid_emails.sort(key=lambda x: x["receivedTime"], reverse=True)

        for email in valid_emails:
            content = email.get("content")
            if content and self.extract_and_save_verification_code(content):
                return

        logger.info("未找到验证码，继续保活")
        self.start_keep_alive()

    def extract_and_save_verification_code(self, content):
        """提取验证码并保存"""
        code = self.extract_verification_code(content)
        if code:
            self.verification_code = code
            YamlTool("common/mail/mail.yaml").update_nested_value("userRegisterInfoPro", "verifyCode", code)
            logger.info(f"提取到验证码: {code}")
            self.stop_keep_alive()
            self.close_connection()
            return True
        return False

    @staticmethod
    def extract_verification_code(content):
        """从邮件内容中提取验证码"""
        match = re.search(r"verification code:\s*<strong>(\d+)</strong>", content)
        return match.group(1) if match else None

    # ========== 保活逻辑 ==========
    def start_keep_alive(self):
        """启动保活"""
        if not self.keep_alive_running:
            self.keep_alive_running = True
            self.keep_alive_attempts = 0
            logger.info("保活线程启动")
            self.schedule_keep_alive()

    def schedule_keep_alive(self):
        """计划下一次保活"""
        if self.keep_alive_running:
            self.keep_alive_timer = Timer(self.KEEP_ALIVE_INTERVAL, self.keep_alive_loop)
            self.keep_alive_timer.start()

    def keep_alive_loop(self):
        """保活操作逻辑"""
        if self.found_verification_code:
            logger.warning("验证码已找到，停止保活")
            self.stop_keep_alive()
            return

        if self.keep_alive_attempts >= self.MAX_KEEP_ALIVE_ATTEMPTS:
            logger.info("保活尝试达到最大次数，重新请求邮件列表")
            self.send_message({"event": "LIST_MAIL"})
            self.stop_keep_alive()
        else:
            self.keep_alive_attempts += 1
            logger.info(f"发送保活信号，第 {self.keep_alive_attempts} 次")
            self.send_message({"bt": "bt"})
            self.schedule_keep_alive()

    def stop_keep_alive(self):
        """停止保活"""
        if self.keep_alive_running:
            self.keep_alive_running = False
            if self.keep_alive_timer:
                self.keep_alive_timer.cancel()
            logger.info("保活线程停止")

    # ========== WebSocket 操作 ==========
    def send_message(self, message):
        """发送 WebSocket 消息"""
        logger.info(f"发送消息: {message}")
        with self.lock:
            if self.ws:
                self.ws.send(json.dumps(message))

    def close_connection(self):
        """关闭 WebSocket 连接"""
        if self.ws:
            self.ws.close()

    # ========== 主线程管理 ==========
    def stop_main_thread(self):
        """停止主线程"""
        self.stop_keep_alive()
        self.close_connection()
        if self.main_thread_timer:
            self.main_thread_timer.cancel()
        logger.info("主线程已停止")

    # ========== 启动方法 ==========
    def start_with_new_account(self):
        """使用新账户启动 WebSocket"""
        self.ws = websocket.WebSocketApp(self.URL,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.main_thread_timer = Timer(self.TIME_LIMIT, self.stop_main_thread)
        self.main_thread_timer.start()
        self.ws.run_forever()

    def get_verification_code(self):
        """获取验证码供外部调用"""
        return self.verification_code


# 调用示例
if __name__ == "__main__":
    client = WebSocketClient()
    client.start_with_new_account()
    verification_code = client.get_verification_code()
    print(f"获取到的验证码: {verification_code}")
