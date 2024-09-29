#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  遍历config文件夹内全部yaml文件获取配置数据
 @time        :  2023/10/18 17:13
"""

import os
import yaml

from common.logger.logTool import logger
from common.pathTool import PathTool


class YamlTool(object):

    """
    YamlEditor类提供了对YAML文件进行增、删、改、查以及处理嵌套键值对的功能。
    """

    def __init__(self, file_path):
        """
        初始化方法，加载YAML文件内容。
        :param file_path: YAML文件的路径
        """
        self.file_path = PathTool.get_splicing_path(file_path)
        self.data = self.load_yaml()

    def load_yaml(self):
        """
        加载YAML文件并返回内容。
        :return: 返回YAML文件内容（字典格式）。
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file) or {}  # 返回字典或空字典
        return {}

    def save_yaml(self):
        """
        保存当前内存中的YAML数据到文件。
        """
        with open(self.file_path, 'w', encoding='utf-8') as file:
            yaml.safe_dump(self.data, file, default_flow_style=False, allow_unicode=True)

    def add(self, key, value):
        """
        添加或更新YAML文件中的键值对。
        :param key: 键
        :param value: 值
        """
        self.data[key] = value
        self.save_yaml()

    def delete(self, key):
        """
        删除YAML文件中的键值对。
        :param key: 要删除的键
        """
        if key in self.data:
            del self.data[key]
            self.save_yaml()
        else:
            logger.error(f"{key} 不存在")

    def update(self, key, value):
        """
        更新YAML文件中的值。
        :param key: 要更新的键
        :param value: 新值
        """
        if key in self.data:
            self.data[key] = value
            self.save_yaml()
        else:
            logger.error(f"{key} 不存在")

    def get(self, key):
        """
        获取YAML文件中的值。
        :param key: 要获取的键
        :return: 返回对应的值
        """
        return self.data.get(key, None)

    def display(self):
        """
        显示当前的YAML文件内容。
        """
        return self.data

    def get_nested_value(self, parent_key, child_key):
        """
        获取嵌套键中的值。例如：获取desired_caps_mi6中的platformVersion。
        :param parent_key: 父键，例如desired_caps_mi6
        :param child_key: 子键，例如platformVersion
        :return: 返回子键对应的值
        """
        if parent_key in self.data and isinstance(self.data[parent_key], dict):
            return self.data[parent_key].get(child_key, None)
        else:
            logger.error(f"{parent_key} 不存在或者不是字典")

    def update_nested_value(self, parent_key, child_key, new_value):
        """
        更新嵌套键中的值。例如：更新desired_caps_mi6中的platformVersion。
        :param parent_key: 父键，例如desired_caps_mi6
        :param child_key: 子键，例如platformVersion
        :param new_value: 新值
        """
        if parent_key in self.data and isinstance(self.data[parent_key], dict):
            self.data[parent_key][child_key] = new_value
            self.save_yaml()
        else:
            logger.error(f"{parent_key} 不存在或者不是字典")


# 测试获取yaml配置数据
if __name__ == '__main__':
    # 加载YAML文件
    yaml_editor = YamlTool('config/example.yaml')

    print(yaml_editor.get("desired_caps_poco"))
    # 获取 YAML 编辑器的显示结果，并记录日志
    try:
        display_result = yaml_editor.display()
        logger.info(display_result)
    except Exception as e:
        logger.error("获取 YAML 显示结果时发生错误: %s", str(e))

    # 获取desired_caps_mi6中的platformVersion值
    platform_version = yaml_editor.get_nested_value('desired_caps_poco', 'platformVersion')
    print(platform_version)  # 输出：9

    yaml_editor.update_nested_value('desired_caps_mi6', 'platformVersion', 10)

    # 验证更新是否成功
    updated_version = yaml_editor.get_nested_value('desired_caps_mi6', 'platformVersion')
    print(updated_version)  # 输出：10


