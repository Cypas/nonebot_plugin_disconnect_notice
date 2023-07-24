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
