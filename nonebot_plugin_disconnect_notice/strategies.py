import time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

import aiosmtplib
import httpx

from nonebot import logger
from .notice_strategy import NoticeStrategy
from .utils import AsHttpReq, sc_send, feishu_gen_sign


class MailStrategy(NoticeStrategy):
    """邮件通知策略"""

    def check_params(self) -> bool:
        return bool(self.config.user and self.config.password and 
                   self.config.server and self.config.port and 
                   self.config.notice_email)

    async def send(self, title: str, content: str) -> Optional[str]:
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = Header(title, 'utf-8')
            message["From"] = self.config.user
            message["To"] = self.config.notice_email
            message.attach(MIMEText(content))

            use_tls = self.config.port == 465
            async with aiosmtplib.SMTP(
                hostname=self.config.server, 
                port=self.config.port, 
                use_tls=use_tls
            ) as smtp:
                await smtp.login(self.config.user, self.config.password)
                await smtp.send_message(message)

            logger.info("通知邮件发送成功!")
            return None
        except Exception as e:
            err = f"邮件发送失败,错误信息如下{e}"
            logger.error(err)
            return err


class PushPlusStrategy(NoticeStrategy):
    """PushPlus通知策略"""

    def check_params(self) -> bool:
        return bool(self.config.token)

    async def send(self, title: str, content: str) -> Optional[str]:
        try:
            url = "http://www.pushplus.plus/send"
            json_data = {
                "token": self.config.token,
                "title": title,
                "content": content,
                "template": "txt",
                "channel": "wechat"
            }

            r = await AsHttpReq.post(url, json=json_data)
            if r.status_code == 200:
                r_json = r.json()
                if r_json["code"] == 200:
                    logger.info("pushplus通知成功!")
                    return None
                else:
                    err = f"pushplus通知失败,res:{r.text}"
                    logger.error(err)
                    return err
            else:
                err = f"pushplus通知失败,res:{r.text}"
                logger.error(err)
                return err
        except (httpx.ConnectError, httpx.ConnectTimeout):
            err = "pushplus通知失败,bot服务器网络错误"
            logger.error(err)
            return err
        except Exception as e:
            err = f"pushplus通知失败,错误信息如下{e}"
            logger.error(err)
            return err


class ServerStrategy(NoticeStrategy):
    """Server酱Turbo通知策略"""

    def check_params(self) -> bool:
        return bool(self.config.key)

    async def send(self, title: str, content: str) -> Optional[str]:
        try:
            options = {"noip": 1, "channel": 9}
            r = await sc_send(
                sendkey=self.config.key, 
                title=title, 
                desp=content, 
                options=options
            )

            if r.status_code == 200:
                r_json = r.json()
                if r_json["code"] == 0:
                    logger.info("server酱Turbo通知成功!")
                    return None
                else:
                    err = f"server酱Turbo通知失败,res:{r.text}"
                    logger.error(err)
                    return err
            else:
                err = f"server酱Turbo通知失败,res:{r.text}"
                logger.error(err)
                return err
        except (httpx.ConnectError, httpx.ConnectTimeout):
            err = "server酱Turbo通知失败,bot服务器网络错误"
            logger.error(err)
            return err
        except Exception as e:
            err = f"server酱Turbo通知失败,错误信息如下{e}"
            logger.error(err)
            return err


class Server3Strategy(NoticeStrategy):
    """Server酱3通知策略"""

    def check_params(self) -> bool:
        return bool(self.config.key)

    async def send(self, title: str, content: str) -> Optional[str]:
        try:
            r = await sc_send(
                sendkey=self.config.key, 
                title=title, 
                desp=content
            )

            if r.status_code == 200:
                r_json = r.json()
                if r_json["code"] == 0:
                    logger.info("server酱3通知成功!")
                    return None
                else:
                    err = f"server酱3通知失败,res:{r.text}"
                    logger.error(err)
                    return err
            else:
                err = f"server酱3通知失败,res:{r.text}"
                logger.error(err)
                return err
        except (httpx.ConnectError, httpx.ConnectTimeout):
            err = "server酱3通知失败,bot服务器网络错误"
            logger.error(err)
            return err
        except Exception as e:
            err = f"server酱3通知失败,错误信息如下{e}"
            logger.error(err)
            return err


class PushOverStrategy(NoticeStrategy):
    """PushOver通知策略"""

    def check_params(self) -> bool:
        return bool(self.config.token and self.config.user_key)

    async def send(self, title: str, content: str) -> Optional[str]:
        try:
            url = "https://api.pushover.net/1/messages.json"
            json_data = {
                "token": self.config.token,
                "user": self.config.user_key,
                "title": title,
                "message": content
            }

            r = await AsHttpReq.post(url, json=json_data)
            if r.status_code == 200:
                r_json: dict = r.json()
                if r_json["status"] == 1 and (r_json.get("info") is None):
                    logger.info("pushover通知成功!")
                    return None
                else:
                    err = f"pushover通知失败,res:{r.text}"
                    logger.error(err)
                    return err
            else:
                err = f"pushover通知失败,res:{r.text}"
                logger.error(err)
                return err
        except (httpx.ConnectError, httpx.ConnectTimeout):
            err = "pushover通知失败,bot服务器网络错误"
            logger.error(err)
            return err
        except Exception as e:
            err = f"pushover通知失败,错误信息如下{e}"
            logger.error(err)
            return err


class FeiShuStrategy(NoticeStrategy):
    """飞书通知策略"""

    def check_params(self) -> bool:
        return bool(self.config.webhook_url)

    async def send(self, title: str, content: str) -> Optional[str]:
        try:
            webhook_url = self.config.webhook_url
            secret = self.config.is_have_secret()

            body = {
                "msg_type": "text",
                "content": {
                    "text": f"{title}\n{content}"
                }
            }

            if secret:
                timestamp = str(int(time.time()))
                sign = feishu_gen_sign(timestamp, secret)
                body["timestamp"] = timestamp
                body["sign"] = sign

            r = await AsHttpReq.post(webhook_url, json=body)
            if r.status_code == 200:
                r_json = r.json()
                if r_json["code"] == 0:
                    logger.info("飞书通知成功!")
                    return None
                else:
                    err = f"飞书通知失败,res:{r.text}"
                    logger.error(err)
                    return err
            else:
                err = f"飞书通知失败,res:{r.text}"
                logger.error(err)
                return err
        except (httpx.ConnectError, httpx.ConnectTimeout):
            err = "飞书通知失败,bot服务器网络错误"
            logger.error(err)
            return err
        except Exception as e:
            err = f"飞书通知失败,错误信息如下{e}"
            logger.error(err)
            return err
