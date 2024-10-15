import json
import time
import websocket
import re
from threading import Timer
from common.logger.logTool import logger


class WebSocketClient:
    URL = "wss://mail.ipwangxin.cn/ws/email"  # 固定 URL

    def __init__(self):
        self.ws = None
        self.account = None
        self.keep_alive_timer = None
        self.keep_alive_count = 0  # 用于计数保活请求次数
        self.found_verification_code = False  # 用于标识是否找到验证码
        self.verification_code = None  # 验证码存储

    def on_open(self, ws):
        logger.info("WebSocket 连接已打开")
        self.send_message(json.dumps({"event": "DOMAIN_NAME"}))  # 第一次发送默认数据请求

    def on_existing_account_message(self, ws, message):
        logger.info(f"收到消息: {message}")
        data = json.loads(message)

        if data.get("event") == "DOMAIN_NAME":
            logger.info(f"域名获取成功: {data.get('data')}")
            self.send_message(json.dumps({"userName": "98e999e4d2", "event": "REGISTER"}))  # 第二次发送注册数据

        elif data.get("event") == "REGISTER" and data.get("data") == True:
            logger.info("注册成功，获取邮件列表")
            self.send_message(json.dumps({"event": "LIST_MAIL"}))  # 第三次请求LIST_MAIL

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
                    self.verification_code = code
                    self.found_verification_code = True
                    self.stop_keep_alive()
                    self.ws.close()  # 关闭WebSocket连接

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
                    self.verification_code = code
                    self.found_verification_code = True
                    self.stop_keep_alive()
                    self.ws.close()  # 关闭WebSocket连接

    def start_with_existing_account(self):
        """使用现有账户启动"""
        self.ws = websocket.WebSocketApp(self.URL,
                                         on_open=self.on_open,
                                         on_message=self.on_existing_account_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.run_forever()

    def start_with_new_account(self):
        """使用新账户启动"""
        self.ws = websocket.WebSocketApp(self.URL,
                                         on_open=self.on_open,
                                         on_message=self.on_new_account_message,  # 处理新账户的消息
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.run_forever()

    def start_keep_alive(self):
        """开始保活，每10秒发送一次请求，持续2分钟"""
        self.keep_alive_timer = Timer(10, self.keep_alive_loop)
        self.keep_alive_timer.start()

    def keep_alive_loop(self):
        """保活循环，每10秒发送一次，持续2分钟"""
        end_time = time.time() + 120  # 保持2分钟
        while time.time() < end_time:
            if self.found_verification_code:  # 如果找到验证码，退出循环
                logger.info("找到验证码，退出保活进程")
                break

            self.keep_alive_count += 1
            if self.keep_alive_count % 3 == 0:
                # 每发送三次保活请求后，发送一次 LIST_MAIL 请求
                logger.info("发送 LIST_MAIL 请求以检查邮件")
                self.send_message(json.dumps({"event": "LIST_MAIL"}))
            else:
                # 否则发送 bt 保活请求
                logger.info("发送保活请求: {'bt': 'bt'}")
                self.send_message(json.dumps({"bt": "bt"}))

            time.sleep(10)

    def stop_keep_alive(self):
        """停止保活"""
        if self.keep_alive_timer:
            self.keep_alive_timer.cancel()
            logger.info("保活停止")

    def get_verification_code(self):
        """获取验证码供外部调用"""
        return self.verification_code


# 调用示例
if __name__ == "__main__":
    client = WebSocketClient()
    client.start_with_existing_account()

    # 等待获取验证码
    while client.get_verification_code() is None:
        time.sleep(1)

    verification_code = client.get_verification_code()
    print(f"获取到的验证码: {verification_code}")
