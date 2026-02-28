from abc import ABC, abstractmethod


class BaseConfig(ABC):
    """配置基类,定义所有配置类的共同接口"""
    
    @abstractmethod
    def check_params(self) -> bool:
        """检查参数是否填写完整"""
        pass


class MailConfig(BaseConfig):
    def __init__(self,
                 user: str,
                 password: str,
                 server: str,
                 port: int,
                 notice_email: str):
        self.user = user
        self.password = password
        self.server = server
        self.port = port
        self.notice_email = notice_email

    def check_params(self) -> bool:
        """检查参数是否填写完整"""
        return bool(self.user and self.password and self.server and self.port and self.notice_email)


# https://www.pushplus.plus/doc/
class PushPlusConfig(BaseConfig):
    def __init__(self, token: str):
        self.token = token

    def check_params(self) -> bool:
        """检查参数是否填写完整"""
        return bool(self.token)


# https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot?f_link_type=f_linkinlinenote&flow_extra=eyJpbmxpbmVfZGlzcGxheV9wb3NpdGlvbiI6MCwiZG9jX3Bvc2l0aW9uIjowLCJkb2NfaWQiOiJiNGU5MmI3OGM2NDBkYzk5LTIzNmNkY2VmNmQ1NGFmOTYifQ%3D%3D&lang=zh-CN
class FeiShuConfig(BaseConfig):
    def __init__(self, webhook_url: str, secret=""):
        self.webhook_url = webhook_url
        self.secret = secret

    def check_params(self) -> bool:
        """检查参数是否填写完整"""
        return bool(self.webhook_url)

    def is_have_secret(self):
        """是否使用了请求鉴权"""
        return self.secret


# https://sct.ftqq.com/
class ServerConfig(BaseConfig):
    def __init__(self, key: str):
        self.key = key

    def check_params(self) -> bool:
        """检查参数是否填写完整"""
        return bool(self.key)


# https://sct.ftqq.com/
class Server3Config(BaseConfig):
    def __init__(self, key: str):
        self.key = key

    def check_params(self) -> bool:
        """检查参数是否填写完整"""
        return bool(self.key)


# https://pushover.net/api#messages
class PushOverConfig(BaseConfig):
    def __init__(self, user_key: str, token: str):
        self.user_key = user_key
        self.token = token

    def check_params(self) -> bool:
        """检查参数是否填写完整"""
        return bool(self.token and self.user_key)


class BotParams:
    def __init__(self,
                 adapter_name: str,
                 bot_id: str,
                 tag: str = None,
                 ):
        self.adapter_name = adapter_name
        self.bot_id = bot_id
        self.tag = tag
