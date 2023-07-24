import smtplib
from email.mime import text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Union

# onebot11 协议
from nonebot.adapters.onebot.v11 import Bot as V11Bot

from nonebot import logger
from .config import plugin_config
from .dataClass import MailConfig

mail_config: MailConfig = MailConfig(
    user=plugin_config.disconnect_notice_smtp_user,
    password=plugin_config.disconnect_notice_smtp_password,
    server=plugin_config.disconnect_notice_smtp_server,
    port=plugin_config.disconnect_notice_smtp_port,
    notice_email=plugin_config.disconnect_notice_notice_email,
)


def send_notice(bot: Union[V11Bot]):
    """整合发送通知消息"""
    bot_id = get_bot_id(bot)
    send_mail(bot_id)


def send_mail(bot_id: str, test: bool = False):
    """发送邮件通知"""
    # 邮箱凭据
    global mail_config
    # 参数校验
    if not mail_config.check_params():
        error = "邮件通知缺少配置参数，无法进行通知"
        logger.error(error)
        return error
    # 邮件正文
    subject = f"你的QQbot掉线了"
    content = f"你的QQbot账号: {bot_id} 掉线了，可能是被风控了，赶快去看看吧"
    if test:
        subject = f"掉线通知测试"
        content = f"这是一封掉线通知测试邮件，你bot并没有掉线"

    # 构造邮件内容
    message = MIMEMultipart("alternative")
    message["Subject"] = Header(subject, 'utf-8')
    message["From"] = mail_config.user
    message["To"] = mail_config.notice_email
    message.attach(MIMEText(content))
    # 连接SMTP服务器并发送邮件
    if mail_config.port == 465:
        server = smtplib.SMTP_SSL(mail_config.server, mail_config.port)
    else:
        # 25或其他
        server = smtplib.SMTP(mail_config.server, mail_config.port)
    try:
        server.login(mail_config.user, mail_config.password)
        server.sendmail(mail_config.user, mail_config.notice_email, message.as_string())
    except Exception as e:
        logger.error(f"邮件发送失败，错误信息如下{e}")
        return e
    logger.info("通知邮件发送成功!")
    return


def get_bot_id(bot: Union[V11Bot]) -> str:
    """获取bot_id"""
    bot_id = bot.self_id
    return bot_id
