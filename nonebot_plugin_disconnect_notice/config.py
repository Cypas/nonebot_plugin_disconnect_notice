from typing import List, Optional

from nonebot import get_driver, get_plugin_config
from pydantic import BaseModel


# 其他地方出现的类似 from .. import config，均是从 __init__.py 导入的 Config 实例
class Config(BaseModel):
    # 推送方式list 枚举值:pushplus mail server
    disconnect_notice_mode_list: list[str] = ["server"]

    # 邮件推送
    disconnect_notice_smtp_user: str | int = ""
    disconnect_notice_smtp_password: str | int = ""
    disconnect_notice_smtp_server: str | int = ""
    disconnect_notice_smtp_port: int = 465
    disconnect_notice_notice_email: str | int = ""

    # pushplus推送 https://www.pushplus.plus/
    disconnect_notice_pushplus_token: str = ""

    # server酱 https://sct.ftqq.com/r/1483
    disconnect_notice_server_key: str = ""

    # pushover
    disconnect_notice_pushover_user_key: str = ""
    disconnect_notice_pushover_token: str = ""

    # 其他设定
    disconnect_notice_dev_mode: bool = False # dev开发模式，此模式下仅输出日志，不实际进行通知
    disconnect_notice_max_grace_time: int = 10 # 断连时最大宽限时间:秒 在此期间重连便不会进行通知


driver = get_driver()
# 本地测试时由于不启动 driver，需要将下面两行注释并取消再下一行的注释
global_config = driver.config
plugin_config = get_plugin_config(Config)

# plugin_config = Config()
