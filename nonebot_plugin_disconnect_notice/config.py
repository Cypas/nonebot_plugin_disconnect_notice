from typing import List, Optional

from nonebot import get_driver, get_plugin_config
from pydantic import BaseModel


# 其他地方出现的类似 from .. import config，均是从 __init__.py 导入的 Config 实例
class Config(BaseModel):
    disconnect_notice_smtp_user: str | int = ""
    disconnect_notice_smtp_password: str = ""
    disconnect_notice_smtp_server: str | int = ""
    disconnect_notice_smtp_port: int = 465
    disconnect_notice_notice_email: str | int = ""
    disconnect_notice_dev_mode: bool = False
    disconnect_notice_max_grace_time: int = 10


driver = get_driver()
# 本地测试时由于不启动 driver，需要将下面两行注释并取消再下一行的注释
global_config = driver.config
plugin_config = get_plugin_config(Config)

# plugin_config = Config()
