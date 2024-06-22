class MailConfig:
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
        if self.user and self.password and self.server and self.port and self.notice_email:
            return True
        else:
            return False

# https://www.pushplus.plus/doc/
class PushPlusConfig:
    def __init__(self,
                 token: str
                 ):
        self.token = token

    def check_params(self) -> bool:
        """检查参数是否填写完整"""
        if self.token:
            return True
        else:
            return False

class ServerConfig:
    def __init__(self,
                 key: str
                 ):
        self.key = key

    def check_params(self) -> bool:
        """检查参数是否填写完整"""
        if self.key:
            return True
        else:
            return False


class BotParams:
    def __init__(self,
                 adapter_name: str,
                 bot_id: str,
                 ):
        self.adapter_name = adapter_name
        self.bot_id = bot_id

