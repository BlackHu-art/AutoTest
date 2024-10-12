import datetime
import re
import time
from urllib.parse import urlencode
import random
import string
import requests

__all__ = ["EmailClient", "EmailDataObject"]


class EmailDataObject(object):
    """邮件对象"""

    def __init__(self, obj, client=None):
        self.obj = obj
        self.subject = obj["SUBJECT"]
        self.sendtime = self.strptime(obj["SENDTIME"])
        self.to_name, self.to_addr = self.email_name(obj["TO"])
        self.from_name, self.from_addr = self.email_name(obj["FROM"])
        self.isread = obj["ISREAD"] != 0
        self._id = obj["MID"]
        self._content = obj.get("CONTENT")
        self._client = client

    @property
    def content(self):
        if not self._content and self._client:
            self.obj["CONTENT"] = self._client.req_api("mailinfo", dict(f=self._id))[1][0]["DATA"][1]
        return self._content

    def email_name(self, name):
        match = re.search("^(.*)<(.+)>$", name)
        name, addr = match.group(1), match.group(2)
        return name or addr, addr

    def strptime(self, string):
        return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return "%(subject)s - %(from_name)s<%(from_addr)s> %(sendtime)s" % dict(
            subject=self.subject,
            from_name=self.from_name,
            from_addr=self.from_addr,
            sendtime=self.sendtime
        )

    def __repr__(self):
        return "<%(classname)s %(subject)s from %(address)s>" % dict(
            classname=self.__module__ + "." + self.__class__.__name__,
            subject=self.subject,
            address=self.from_addr
        )



class EmailClient(object):
    """基于24mail.chacuo.net的一个邮件接收类"""

    base_url = "http://24mail.chacuo.net/"

    def __init__(self, email_generator, session=None):
        self.session = session or requests.Session()
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://24mail.chacuo.net",
            "Referer": "http://24mail.chacuo.net/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": "HMACCOUNT=317F54DC8D3895C9; Hm_lvt_ef483ae9c0f4f800aefdf407e35a21b3=1728545325; sid=5d5251747deb8a9f3d93ed99c3262d1af482c02c; Hm_lpvt_ef483ae9c0f4f800aefdf407e35a21b3=1728717296; mail_ck=22"
        }
        self._name = email_generator.generate_random_name()  # 使用生成器生成邮箱名
        self.subfix = email_generator.subfix
        self.session.get(self.base_url, headers=self.headers)
        # 调用API设置邮箱域名
        response = self.req_api("set", dict(d=self.subfix))
        if response is None:
            raise Exception("无法设置邮箱域名，请检查网络连接或服务是否可用")

    def receive(self):
        """接收邮件"""
        data = self.req_api()
        return data.get("list") if data else []

    def req_api(self, type="refresh", arg=None):
        """请求API，并处理返回结果"""
        try:
            params = dict(
                data=self.name,
                type=type,
                arg=urlencode(arg or dict()).replace("&", "_")
            )
            response = self.session.post(self.base_url, headers=self.headers, data=params)
            if response.status_code != 200:
                print(f"HTTP错误: {response.status_code}")
                return None
            return response.json().get("data").pop()
        except requests.RequestException as e:
            print(f"请求发生错误: {e}")
            return None

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self.name + "@" + self.subfix


# 调用示例
if __name__ == '__main__':
    client = EmailClient()
    print(f"邮箱地址: {client.address}")

    timeout = 120  # 监听2分钟
    interval = 5  # 间隔5秒
    start_time = time.time()

    while True:
        emails = client.receive()

        if emails:
            for email in emails:
                print(f"邮件主题: {email.subject}")
                print(f"发件人: {email.from_addr}")
                print(f"发送时间: {email.sendtime}")
                print(f"邮件内容: {email.content}")
            break  # 收到邮件后结束循环
        elif time.time() - start_time > timeout:
            raise TimeoutError("2分钟内没有收到邮件，监听超时")
        else:
            print("未收到邮件，继续监听...")
            time.sleep(interval)
