import time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

import aiosmtplib

from nonebot import logger, Bot
from .config import plugin_config
from .dataClass import MailConfig, BotParams, PushPlusConfig, ServerConfig, PushOverConfig, Server3Config, FeiShuConfig
from .utils import *

mail_config: MailConfig = MailConfig(
    user=plugin_config.disconnect_notice_smtp_user,
    password=plugin_config.disconnect_notice_smtp_password,
    server=plugin_config.disconnect_notice_smtp_server,
    port=plugin_config.disconnect_notice_smtp_port,
    notice_email=plugin_config.disconnect_notice_notice_email,
)

pushplus_config: PushPlusConfig = PushPlusConfig(
    token=plugin_config.disconnect_notice_pushplus_token,
)

server_config: ServerConfig = ServerConfig(
    key=plugin_config.disconnect_notice_server_key,
)

server3_config: Server3Config = Server3Config(
    key=plugin_config.disconnect_notice_server3_key,
)

pushover_config: PushOverConfig = PushOverConfig(
    user_key=plugin_config.disconnect_notice_pushover_user_key,
    token=plugin_config.disconnect_notice_pushover_token
)

feishu_config: FeiShuConfig = FeiShuConfig(
    webhook_url=plugin_config.disconnect_notice_feishu_webhook_url,
    secret=plugin_config.disconnect_notice_feishu_secret,
)


def check_params(platform: str) -> Optional[str]:
    """多平台检查配置参数完整性"""
    err = "{platform} 平台通知缺少配置参数，无法进行通知，\n" \
          "请参考https://github.com/Cypas/nonebot_plugin_disconnect_notice#%EF%B8%8F-%E9%85%8D%E7%BD%AE\n" \
          "填写该推送方式配置项"
    if platform == PLATFORM_PUSHPLUS:
        if not pushplus_config.check_params():
            return err.format(platform=platform)
    elif platform == PLATFORM_MAIL:
        if not mail_config.check_params():
            return err.format(platform=platform)
    elif platform == PLATFORM_SERVER:
        if not server_config.check_params():
            return err.format(platform=platform)
    elif platform == PLATFORM_SERVER3:
        if not server3_config.check_params():
            return err.format(platform=platform)
    elif platform == PLATFORM_PUSHOVER:
        if not pushover_config.check_params():
            return err.format(platform=platform)
    elif platform == PLATFORM_FEISHU:
        if not feishu_config.check_params():
            return err.format(platform=platform)
    return None


async def send_notice(bot_params: BotParams, test=False):
    """整合发送通知消息"""
    mode_list = plugin_config.disconnect_notice_mode_list
    err = None

    ## 消息主体
    if not test:
        title = f"[nonebot2]你的bot掉线了"
        if not bot_params.tag:
            content = f"你的 {bot_params.adapter_name} 适配器的bot账号: {bot_params.bot_id} 掉线了，可能是被风控了，赶快去看看吧"
        else:
            content = f"你的 {bot_params.adapter_name} 适配器的bot账号: {bot_params.bot_id} 掉线了，原因为: {bot_params.tag} 。赶快去看看吧"
    else:
        title = f"[nonebot2]掉线通知测试"
        content = f"这是一个掉线通知测试信息，你的bot并没有掉线"

    # pushplus
    if PLATFORM_PUSHPLUS in mode_list:
        platform = PLATFORM_PUSHPLUS
        # 参数校验
        err = check_params(platform)
        if not err:
            err = await send_pushplus(title, content)
        if err:
            logger.error(err)

    # mail
    if PLATFORM_MAIL in mode_list:
        platform = PLATFORM_MAIL
        # 参数校验
        err = check_params(platform)
        if not err:
            err = await send_mail(title, content)
        if err:
            logger.error(err)

    # server Turbo
    if PLATFORM_SERVER in mode_list:
        platform = PLATFORM_SERVER
        # 参数校验
        err = check_params(platform)
        if not err:
            err = await send_server(title, content)
        if err:
            logger.error(err)

    # server3
    if PLATFORM_SERVER3 in mode_list:
        platform = PLATFORM_SERVER3
        # 参数校验
        err = check_params(platform)
        if not err:
            err = await send_server3(title, content)
        if err:
            logger.error(err)

    # pushover
    if PLATFORM_PUSHOVER in mode_list:
        platform = PLATFORM_PUSHOVER
        # 参数校验
        err = check_params(platform)
        if not err:
            err = await send_pushover(title, content)
        if err:
            logger.error(err)

    # feishu
    if PLATFORM_FEISHU in mode_list:
        platform = PLATFORM_FEISHU
        # 参数校验
        err = check_params(platform)
        if not err:
            err = await send_feishu(title, content)
        if err:
            logger.error(err)
    return err


async def send_server(title: str, content: str):
    """发送server酱Turbo微信公众号通知"""
    send_key = server_config.key
    options = {
        "noip": 1,
        "channel": 9
    }
    try:
        r = await sc_send(sendkey=send_key, title=title, desp=content, options=options)
        if r.status_code == 200:
            r_json = r.json()
            if r_json["code"] == 0:
                logger.info("server酱Turbo通知成功!")
            else:
                err = f"server酱Turbo通知失败，res:{r.text}"
                return err
    except (httpx.ConnectError, httpx.ConnectTimeout):
        err = f"server酱Turbo通知失败，bot服务器网络错误"
        return err
    except Exception as e:
        err = f"server酱Turbo通知失败，错误信息如下{e}"
        return err
    return None


async def send_server3(title: str, content: str):
    """发送server酱3通知"""
    send_key = server3_config.key
    try:
        r = await sc_send(sendkey=send_key, title=title, desp=content)
        if r.status_code == 200:
            r_json = r.json()
            if r_json["code"] == 0:
                logger.info("server酱3通知成功!")
            else:
                err = f"server酱3通知失败，res:{r.text}"
                return err
    except (httpx.ConnectError, httpx.ConnectTimeout):
        err = f"server酱3通知失败，bot服务器网络错误"
        return err
    except Exception as e:
        err = f"server酱3通知失败，错误信息如下{e}"
        return err
    return None


async def send_pushplus(title: str, content: str):
    """发送pushplus微信公众号通知"""
    url = "http://www.pushplus.plus/send"
    json = {"token": pushplus_config.token,
            "title": title,
            "content": content,
            "template": "txt",
            "channel": "wechat"
            }
    try:
        r = await AsHttpReq.post(url, json=json)
        if r.status_code == 200:
            r_json = r.json()
            if r_json["code"] == 200:
                logger.info("pushplus通知成功!")
            else:
                err = f"pushplus通知失败，res:{r.text}"
                return err
    except (httpx.ConnectError, httpx.ConnectTimeout):
        err = f"pushplus通知失败，bot服务器网络错误"
        return err
    except Exception as e:
        err = f"pushplus通知失败，错误信息如下{e}"
        return err
    return None


async def send_mail(title: str, content: str):
    """发送邮件通知"""
    # 构造邮件内容
    message = MIMEMultipart("alternative")
    message["Subject"] = Header(title, 'utf-8')
    message["From"] = mail_config.user
    message["To"] = mail_config.notice_email
    message.attach(MIMEText(content))
    # 连接SMTP服务器并发送邮件
    use_tls = False
    if mail_config.port == 465:
        use_tls = True
    try:
        async with aiosmtplib.SMTP(hostname=mail_config.server, port=mail_config.port, use_tls=use_tls) as smtp:
            await smtp.login(mail_config.user, mail_config.password)
            await smtp.send_message(message)
    except Exception as e:
        err = f"邮件发送失败，错误信息如下{e}"
        return err
    logger.info("通知邮件发送成功!")
    return None


async def send_pushover(title: str, content: str):
    """发送pushover通知"""
    url = "https://api.pushover.net/1/messages.json"
    json = {"token": pushover_config.token,
            "user": pushover_config.user_key,
            "title": title,
            "message": content
            }

    r = await AsHttpReq.post(url, json=json)
    if r.status_code == 200:
        r_json: dict = r.json()
        if r_json["status"] == 1 and (r_json.get("info") is None):
            logger.info("pushover通知成功!")
        else:
            err = f"pushover通知失败，res:{r.text}"
            return err

    return None


async def send_feishu(title: str, content: str):
    """发送飞书 webhook通知"""
    webhook_url = feishu_config.webhook_url
    secret = feishu_config.is_have_secret()
    body = {
        "msg_type": "text",
        "content": {
            "text": f"{title}\n{content}"
        }
    }
    if secret:
        # 若使用了请求加密
        timestamp = str(int(time.time()))
        sign = feishu_gen_sign(timestamp, secret)
        body["timestamp"] = timestamp
        body["sign"] = sign
    try:
        r = await AsHttpReq.post(webhook_url, json=body)
        if r.status_code == 200:
            r_json = r.json()
            if r_json["code"] == 0:
                logger.info("飞书通知成功!")
            else:
                err = f"飞书通知失败，res:{r.text}"
                return err
    except (httpx.ConnectError, httpx.ConnectTimeout):
        err = f"飞书通知失败，bot服务器网络错误"
        return err
    except Exception as e:
        err = f"飞书通知失败，错误信息如下{e}"
        return err
    return None
