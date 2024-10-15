#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  
 @time        :    16:24
"""
import random
import string
from common.yamlTool import YamlTool
from common.logger.logTool import logger


class EmailGenerator:
    """生成随机邮箱账号的类"""

    def __init__(self, length=11, prefix="", subfix="@ipwangxin.cn"):
        self.length = length
        self.prefix = prefix
        self.subfix = subfix

    def generate_email_prename(self):
        """生成随机邮箱名"""
        prename = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(self.length))
        logger.info("随机生成的邮箱名前缀：%s" % prename)
        return prename

    def get_email_address(self):
        """返回完整的邮箱地址"""
        random_name = self.prefix + self.generate_email_prename()
        return random_name + "@" + self.subfix


if __name__ == "__main__":
    print(EmailGenerator().generate_email_prename())