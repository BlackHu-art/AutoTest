#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  遍历config文件夹内全部yaml文件获取配置数据
 @time        :  2023/10/18 17:13
"""

import os
import yaml
from yaml import FullLoader

from logger import logger
from common.pathTool import PathTool


class YamlUtil(object):
    CONFIG_DIR = PathTool.get_config_dir()

    def load_yaml_configs(self, filename=None):
        """
        加载YAML配置文件。

        :param filename: 要加载的特定文件名
        :return: 文件中的配置数据
        """
        if filename is not None:
            # 验证文件名是否安全
            if not self.is_safe_filename(filename):
                raise ValueError("Invalid filename provided.")

            file_path = os.path.join(self.CONFIG_DIR, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    datas = yaml.load(f, Loader=FullLoader)
                    logger.info(f"成功读取文件 {filename}")
                    return datas
            except Exception as e:
                logger.error(f"读取文件 {filename} 失败: {e}")
                return None

        else:
            logger.error(f"读取文件失败，传参filename为空")
            return

    @staticmethod
    def is_safe_filename(filename):
        """
        检查文件名是否安全。

        :param filename: 文件名
        :return: 是否安全
        """
        return not (os.path.sep in filename or os.path.altsep in filename)

    def clear_data_with_path(self, filename):
        """
        清空指定文件的内容。

        :param filename: 文件名
        """
        if not self.is_safe_filename(filename):
            raise ValueError("Invalid filename provided.")

        file_path = os.path.join(self.CONFIG_DIR, filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.truncate()
                logger.info(f"成功清空文件 {filename}")
        except Exception as e:
            logger.error(f"清空文件 {filename} 失败: {e}")

    def write_to_yaml(self, data, filename):
        """
        将数据写入YAML文件。

        :param data: 要写入的数据
        :param filename: 文件名
        """
        if not self.is_safe_filename(filename):
            raise ValueError("Invalid filename provided.")

        file_path = os.path.join(self.CONFIG_DIR, filename)
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.dump(data, file, allow_unicode=True)
                logger.info(f"成功写入文件 {filename}")
        except Exception as e:
            logger.error(f"写入文件 {filename} 失败: {e}")


# 创建实例并调用示例
yaml_util = YamlUtil()


# 测试获取yaml配置数据
if __name__ == '__main__':
    # 获取特定文件的数据
    specific_file_data = yaml_util.load_yaml_configs("example.yaml")
    print(specific_file_data)

    # 获取所有文件的数据
    all_files_data = yaml_util.load_yaml_configs()
    print(all_files_data)

