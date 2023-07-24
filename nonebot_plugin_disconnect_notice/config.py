from typing import List, Optional

from nonebot import get_driver
from pydantic import BaseModel


# 其他地方出现的类似 from .. import config，均是从 __init__.py 导入的 Config 实例
class Config(BaseModel):
    disconnect_notice_smtp_user = ""
    disconnect_notice_smtp_password = ""
    disconnect_notice_smtp_server = ""
    disconnect_notice_smtp_port = 465
    disconnect_notice_notice_email = ""
    disconnect_notice_dev_mode = False


driver = get_driver()
# 本地测试时由于不启动 driver，需要将下面两行注释并取消再下一行的注释
global_config = driver.config
plugin_config = Config.parse_obj(global_config)

# plugin_config = Config()
