#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @author      :  Frankie
 @description :  生成巴西国家地区的CPF请求头可能会失效，需要更新
 @time        :    9:38
"""
import random
import re
import string

import requests
import time
from common.logger.logTool import logger


class CPFGenerator:
    def __init__(self):
        self.url = "https://www.4devs.com.br/ferramentas_online.php"
        self.headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,pt-BR;q=0.8,pt;q=0.7,en-US;q=0.6,en;q=0.5",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "_ga_7RD2VB3FJH=GS1.1.1730338215.1.0.1730338215.0.0.0; _ga=GA1.1.1160646418.1730338216; FCNEC=%5B%5B%22AKsRol-vAxOc4KP43vTmO5H-F-wN_VbWAg_mckFK1PQqEb-4pZZrXalZCfhuS68GiIZnnMFH6X86fPKJabx7HHaC3th8AwZpKk5vqm2ZpifXh0AttIyK7QvBTMGEWMzE9xjrxFVZmPKRH3ozAOlEqvdVQcqHjNKfsA%3D%3D%22%5D%5D; cto_bundle=ziEOQV9JNnZTZk1SOUFHT1dmTG1vd3JDcXdmUzVUdlNaT05PS3RJNkZWY3BOSU14OWsxZXIlMkZzOU1KNSUyRnl3bzY4ejZLMVVwclpFRiUyRlVMeUdSRGxLTXdvcmVhJTJCajZyc2hUbjZ6TnJQaEl1dFdlVFJ4dTVSRWJDREpoWTdqVVhXUEtxVWpDVkx0NjNmRUdUdnhyVklyck4ybXBVd2xnM1VQbG1RZkpPUXZMMHN5NXB3dkdpOXM3MjZvcks2TkNDQkwlMkJtRTJ2MXZHUjhmblhabm5uaDBRajNmWHI2ZyUzRCUzRA; _clck=17u7kg3%7C2%7Cfqh%7C0%7C1765; _clsk=q4jbc7%7C1730338218922%7C1%7C1%7Cv.clarity.ms%2Fcollect",
            "origin": "https://www.4devs.com.br",
            "priority": "u=1, i",
            "referer": "https://www.4devs.com.br/gerador_de_cpf",
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        self.payload = {
            "acao": "gerar_cpf",
            "pontuacao": "S",
            "cpf_estado": ""
        }

    def generate_cpfs(self, number=1):
        """Generate multiple CPF numbers, remove non-numeric characters, with a 1-second delay between requests."""
        responses = []
        for i in range(number):
            try:
                response = requests.post(self.url, headers=self.headers, data=self.payload)
                if response.status_code == 200:
                    cpf = re.sub(r"\D", "", response.text)  # Remove all non-digit characters
                    logger.info(f"Response {i + 1}: {cpf}")
                    responses.append(cpf)
                else:
                    error_message = f"Error {response.status_code} - Failed to generate CPF"
                    logger.error(error_message)
                    responses.append(error_message)
            except requests.RequestException as e:
                logger.error(f"Request failed: {e}")
                responses.append(f"Request failed: {e}")
            # time.sleep(1)  # Adding delay of 1 second between requests
        return responses

    def save_to_file(self, data, filename="cpf_results.txt"):
        """Save the CPF data to a text file, each result on a new line."""
        try:
            with open(filename, "w") as file:
                for line in data:
                    file.write(line + "\n")
            logger.info(f"Results saved to {filename}")
        except IOError as e:
            logger.error(f"File write error: {e}")


class DataGenerator:
    def __init__(self, num_entries):
        self.num_entries = num_entries
        self.cpf_generator = CPFGenerator()

    def _generate_random_username(self):
        # 生成一个10位随机字符串作为用户名
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

    def generate_data(self):
        data_entries = []
        cpfs = self.cpf_generator.generate_cpfs(self.num_entries)  # 获取生成的 CPF 列表
        for i in range(self.num_entries):
            name = "TESTEDOOZY"
            cpf = cpfs[i] if i < len(cpfs) else "00000000000"  # 若未生成 CPF，用默认值替代
            email = f"{self._generate_random_username()}@ipwangxin.cn"
            first_name = "Nome"
            last_name = "Sobrenome"
            entry = f"{name};{cpf};{email};{first_name};{last_name}"
            data_entries.append(entry)
        return data_entries

    def save_to_file(self, filename="generated_data.txt"):
        data_entries = self.generate_data()
        try:
            with open(filename, 'w') as file:
                for entry in data_entries:
                    file.write(entry + "\n")
            logger.info(f"Results saved to {filename}")
        except IOError as e:
            logger.error(f"File write error: {e}")


# 使用示例
if __name__ == "__main__":
    # num_entries = 5  # 指定生成的数据条数
    generator = DataGenerator(num_entries=50000)
    generator.save_to_file()

#
# # 调用示例
# if __name__ == "__main__":
#     generator = CPFGenerator()
#     cpf_data = generator.generate_cpfs(number=1000)  # 生成5个CPF
#     generator.save_to_file(cpf_data, filename="cpf_results.txt")
