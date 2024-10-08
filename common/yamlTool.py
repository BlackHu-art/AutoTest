#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  遍历config文件夹内全部yaml文件获取配置数据
 @time        :  2023/10/18 17:13
"""

import os
from ruamel.yaml import YAML
from ast import literal_eval
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
        self.yaml = YAML()
        self.yaml.preserve_quotes = True  # 保留引号
        self.data = self._load_yaml()

    def _load_yaml(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = self.yaml.load(f)
                    logger.info(f"加载YAML文件成功: {self.file_path}")
                    return data
            else:
                logger.error(f"文件不存在: {self.file_path}")
                return {}
        except Exception as ex:
            logger.error(f"加载YAML文件失败: {ex}")
            return {}

    def save_yaml(self):
        """
        保存当前内存中的YAML数据到文件。
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                self.yaml.dump(self.data, f)
            logger.info(f"保存YAML文件成功: {self.file_path}")
        except Exception as ex:
            logger.error(f"保存YAML文件失败: {ex}")

    def delete(self, key):
        """
        删除YAML文件中的键值对。
        :param key: 要删除的键
        """
        if key in self.data:
            del self.data[key]
            self.save_yaml()
            logger.info(f"删除键 {key} 在文件 {self.file_path}")
        else:
            logger.warning(f"键 {key} 不存在于文件 {self.file_path}")

    def update(self, key, value):
        """
        更新YAML文件中的值。
        :param key: 要更新的键
        :param value: 新值
        """
        if key in self.data:
            self.data[key] = value
            self.save_yaml()
            logger.info(f"更新键值对: {key} = {value} 在文件 {self.file_path}")
        else:
            logger.warning(f"键 {key} 不存在于文件 {self.file_path}")

    def get(self, key):
        """
        获取YAML文件中的值。
        :param key: 要获取的键
        :return: 返回对应的值
        """
        value = self.data.get(key)
        logger.info(f"获取键 {key} 的值: {value} 在文件 {self.file_path}")
        return value

    def add(self, key, value_str):
        """
        添加一个键值对到 YAML 文件中。如果值是字符串形式的字典，将其解析为字典。
        :param key: 要添加的键
        :param value_str: 字符串形式的值，如果是键值对的字符串，将其解析为字典
        """
        try:
            # 尝试将字符串转换为字典或其他类型的 Python 对象
            value = literal_eval(value_str)
        except (ValueError, SyntaxError):
            # 如果无法转换，保留原始字符串作为值
            value = value_str

        # 将键值对添加到 YAML 数据中
        if key in self.data:
            logger.warning(f"键 {key} 已存在于文件 {self.file_path}，将覆盖其值")

        self.data[key] = value
        self.save_yaml()  # 保存更改到文件
        # logger.info(f"添加键值对: {key} = {value} 到文件 {self.file_path}")

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
        parent_value = self.data.get(parent_key)
        if isinstance(parent_value, dict):
            child_value = parent_value.get(child_key)
            logger.info(f"获取嵌套键 {parent_key}.{child_key} 的值: {child_value} 在文件 {self.file_path}")
            return child_value
        else:
            logger.error(f"父键 {parent_key} 不存在或不是字典类型")
            return None

    def update_nested_value(self, parent_key, child_key, new_value):
        """
        更新嵌套键中的值。例如：更新desired_caps_mi6中的platformVersion。
        :param parent_key: 父键，例如desired_caps_mi6
        :param child_key: 子键，例如platformVersion
        :param new_value: 新值
        """
        parent_value = self.data.get(parent_key)
        if isinstance(parent_value, dict):
            parent_value[child_key] = new_value
            self.save_yaml()
            logger.info(f"更新嵌套键 {parent_key}.{child_key} 的值为: {new_value} 在文件 {self.file_path}")
        else:
            logger.error(f"父键 {parent_key} 不存在或不是字典类型")


# 测试获取yaml配置数据
if __name__ == '__main__':
    # 加载YAML文件
    yaml_editor = YamlTool('config/example.yaml')
    # yaml_editor.add("test_key", "{'app': 'D:\WORK_PY\AutoTest\config\example.yaml', 'appActivity': "
    #                             "'com.mm.droid.livetv.load.LiveLoadActivity', 'appPackage': "
    #                             "'com.mm.droid.livetv.stb31023418', 'deviceName': '10.0.0.132:5188', 'platformName': "
    #                             "'Android', 'platformVersion': 9}")

    # print(yaml_editor.get("desired_caps_poco"))
    # # 获取 YAML 编辑器的显示结果，并记录日志
    # try:
    #     display_result = yaml_editor.display()
    #     logger.info(display_result)
    # except Exception as e:
    #     logger.error("获取 YAML 显示结果时发生错误: %s", str(e))
    #
    # # 获取desired_caps_mi6中的platformVersion值
    # platform_version = yaml_editor.get_nested_value('desired_caps_poco', 'platformVersion')
    #
    # yaml_editor.update_nested_value('desired_caps_mi6', 'noReset', False)
    #
    # # 验证更新是否成功
    # updated_version = yaml_editor.get_nested_value('desired_caps_mi6', 'noReset')

