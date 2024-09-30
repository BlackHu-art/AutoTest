from common.logger import logger
import platform


def deal_pytest_ini_file():
    """
    由于当前(2020/1/15)pytest运行指定的pytest.ini在Windows下编码有bug，故对不同环境进行处理
    """
    try:
        with open('config/pytest.conf', 'r', encoding='utf-8') as pytest_f:
            content = pytest_f.read()

        if platform.system() == 'Windows':
            with open('config/pytest.ini', 'w+', encoding='utf-8-sig') as tmp_pytest_f:
                tmp_pytest_f.write(content)
        else:
            with open('config/pytest.ini', 'w+', encoding='utf-8') as tmp_pytest_f:
                tmp_pytest_f.write(content)

    except Exception as e:
        logger.error(f"Error occurred: {e}")
