class MailConfig:
    def __init__(self,
                 user,
                 password,
                 server,
                 port,
                 notice_email):
        self.user = user
        self.password = password
        self.server = server
        self.port = port
        self.notice_email = notice_email

    def check_params(self) -> bool:
        """检查参数是否填写完整"""
        if not (self.smtp_user or self.smtp_password or self.smtp_server or self.smtp_port or self.notice_email):
            return False
        else:
            return True
