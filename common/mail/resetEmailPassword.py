import json
import websocket
import re
from datetime import datetime, timedelta
from threading import Timer
from common.logger.logTool import logger
from common.yamlTool import YamlTool


class WebSocketClient:
    URL = "wss://mail.ipwangxin.cn/ws/email"
    KEEP_ALIVE_INTERVAL = 6  # 保活间隔时间（秒）
    TIME_LIMIT = 120  # 主线程超时时间（秒）
    MAX_KEEP_ALIVE_ATTEMPTS = 3  # 最大保活次数

    def __init__(self):
        self.ws = None
        self.keep_alive_timer = None
        self.keep_alive_attempts = 0
        self.verification_code = None
        self.found_verification_code = False
        self.main_thread_timer = None
        self.keep_alive_running = False

    def send_message(self, message):
        """发送消息"""
        try:
            message_json = json.dumps(message)
            logger.info(f"发送消息: {message_json}")
            self.ws.send(message_json)
        except Exception as e:
            logger.error(f"发送消息失败: {e}")

    def close_connection(self):
        """关闭 WebSocket 连接"""
        if self.ws:
            logger.info("关闭 WebSocket 连接")
            self.ws.close()

    # ======== WebSocket 事件处理模块 ========
    def on_open(self, ws):
        logger.info("WebSocket 连接已打开")
        self._request_domain_name()

    def on_message(self, ws, message):
        try:
            logger.info(f"收到消息: {message}")
            data = json.loads(message)
            self._handle_event(data)
        except Exception as e:
            logger.error(f"消息处理出错: {e}")

    def on_error(self, ws, error):
        logger.error(f"WebSocket 错误: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logger.info(f"WebSocket 已关闭，状态码: {close_status_code}, 消息: {close_msg}")
        self.stop_keep_alive()

    def _handle_event(self, data):
        """根据事件类型处理消息"""
        event = data.get("event")
        handler_map = {
            "DOMAIN_NAME": self._handle_domain_name,
            "REGISTER": self._handle_register,
            "LIST_MAIL": self._handle_list_mail,
            "NEW_EMAIL": self._handle_new_email,
        }
        handler = handler_map.get(event, self._handle_unknown_event)
        handler(data)

    def _handle_unknown_event(self, data):
        logger.warning(f"未知事件: {data}")

    # ======== 消息处理模块 ========
    def _request_domain_name(self):
        """请求域名信息"""
        self.send_message({"event": "DOMAIN_NAME"})

    def _handle_domain_name(self, data):
        logger.info(f"域名获取成功: {data.get('data')}")
        self._register_account()

    def _register_account(self):
        """注册账户"""
        mail = self.extract_username(YamlTool("common/mail/mail.yaml").get_nested_value("userRegisterInfoPro", "account"))
        self.send_message({"userName": mail, "event": "REGISTER"})

    def extract_username(self, email):
        """
        从邮箱地址中提取用户名部分（@之前的内容）。

        :param email: str, 邮箱地址
        :return: str, 用户名
        """
        match = re.match(r"([^@]+)@.*", email)
        return match.group(1) if match else None

    def _handle_register(self, data):
        if data.get("data") is True:
            logger.info("注册成功，获取邮件列表")
            self._request_list_mail()

    def _request_list_mail(self):
        """请求邮件列表"""
        self.send_message({"event": "LIST_MAIL"})

    def _handle_list_mail(self, data):
        emails = data.get("data", [])
        if not emails:
            logger.info("邮件列表为空，启动保活机制")
            self.start_keep_alive()
        else:
            self._process_emails(emails)

    def _handle_new_email(self, data):
        logger.info("收到新邮件通知")
        content = data.get("data", {}).get("content")
        if content:
            self._extract_verification_code(content)

    # ======== 邮件处理模块 ========
    def _process_emails(self, emails):
        """
        处理邮件列表，提取两分钟内的最新验证码。

        :param emails: list, 响应中的邮件数据
        """
        found_code = False
        current_time = datetime.now()
        two_minutes_ago = current_time - timedelta(minutes=2)

        # 筛选两分钟内的邮件
        valid_emails = [
            email for email in emails
            if "receivedTime" in email and datetime.fromtimestamp(email["receivedTime"] / 1000) > two_minutes_ago
        ]

        # 根据接收时间排序（从最新到最早）
        valid_emails.sort(key=lambda x: x["receivedTime"], reverse=True)

        # 遍历筛选后的邮件提取验证码
        for email in valid_emails:
            content = email.get("content")
            if content:
                code = self._extract_verification_code(content)
                if code:
                    logger.info(f"找到验证码: {code} (邮件接收时间: {email['receivedTime']})")
                    self.verification_code = code
                    found_code = True
                    self.found_verification_code = True  # 设置为已找到验证码
                    self.stop_keep_alive()  # 停止保活
                    self.ws.close()  # 关闭 WebSocket 连接
                    break

        if not found_code:
            logger.info("未找到符合条件的验证码，继续保活")
            self.start_keep_alive()  # 继续保活

    def _extract_verification_code(self, content):
        """提取验证码"""
        code = self._find_verification_code(content)
        if code:
            YamlTool("common/mail/mail.yaml").update_nested_value("userRegisterInfoPro", "verifyCode", code)
            logger.info(f"提取到验证码: {code}")
            self.verification_code = code
            self.found_verification_code = True
            self.close_connection()
            return True
        return False

    @staticmethod
    def _find_verification_code(content):
        """正则匹配验证码"""
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

    # ========== 主线程管理 ==========
    def stop_main_thread(self):
        """停止主线程"""
        self.stop_keep_alive()
        self.close_connection()
        if self.main_thread_timer:
            self.main_thread_timer.cancel()
        logger.info("主线程已停止")

    # ======== WebSocket 管理模块 ========
    def start_with_old_account(self):
        """启动 WebSocket 连接"""
        self.ws = websocket.WebSocketApp(
            self.URL,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.main_thread_timer = Timer(self.TIME_LIMIT, self.stop_main_thread)
        self.main_thread_timer.start()
        self.ws.run_forever()

    # ======== 对外接口 ========
    def get_verification_code(self):
        """获取验证码"""
        return self.verification_code


# ======== 调用示例 ========
if __name__ == "__main__":
    client = WebSocketClient()
    client.start_with_old_account()

    logger.info(f"获取到的验证码: {client.get_verification_code()}")
    # logger.info(client.extract_username(YamlTool("common/mail/mail.yaml").get_nested_value("userRegisterInfoPro", "account")))

