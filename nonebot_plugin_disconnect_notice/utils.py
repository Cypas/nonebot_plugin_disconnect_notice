import smtplib
from email.mime import text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
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


def send_notice(bot: V11Bot):
    """整合发送通知消息"""
    bot_id = get_bot_id(bot)
    if not send_mail(bot):
        # 缺少参数
        super_user: str = plugin_config.SUPERUSERS[0]
        if super_user:
            bot.send_private_msg(super_user, "")


def send_mail(bot_id: str):
    """发送邮件通知"""
    # 邮箱凭据
    global mail_config
    # 参数校验
    if not mail_config.check_params():
        logger.error("邮件通知缺少配置参数，无法进行通知")
        return
    # 邮件正文
    subject = f"你的QQbot掉线了"
    content = f"你的QQbot账号: {bot_id} 掉线了，可能是被风控了，赶快去看看吧"

    # 构造邮件内容
    message = MIMEMultipart("alternative")
    message["Subject"] = Header(subject, 'utf-8')
    message["From"] = smtp_user
    message["To"] = notice_email
    message.attach(MIMEText(content))
    # 连接SMTP服务器并发送邮件
    if smtp_port == 465:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    else:
        # 25或其他
        server = smtplib.SMTP(smtp_server, smtp_port)
    try:
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, notice_email, message.as_string())
    except Exception as e:
        logger.error(f"邮件发送失败，错误信息如下{e}")
        return
    logger.info("通知邮件发送成功!")


def get_bot_id(bot: V11Bot) -> str:
    """获取bot_id"""
    bot_id = bot.self_id
    return bot_id
