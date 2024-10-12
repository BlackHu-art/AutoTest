#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    16:24
"""
import random
import string


class EmailGenerator:
    """生成随机邮箱账号的类"""

    def __init__(self, length=11, prefix="", subfix="@ipwangxin.cn"):
        self.length = length
        self.prefix = prefix
        self.subfix = subfix

    def generate_random_name(self):
        """生成随机邮箱名"""
        return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(self.length))

    def get_email_address(self):
        """返回完整的邮箱地址"""
        random_name = self.prefix + self.generate_random_name()
        return random_name + "@" + self.subfix


if __name__ == "__main__":
    print(EmailGenerator().get_email_address())
    print(EmailGenerator().generate_random_name())