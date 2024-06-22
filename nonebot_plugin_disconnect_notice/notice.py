from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib
import httpx

from nonebot import logger, Bot
from .config import plugin_config
from .dataClass import MailConfig, BotParams, PushPlusConfig
from .utils import AsHttpReq

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


async def send_notice(bot_params: BotParams, test=False):
    """整合发送通知消息"""
    mode_list = plugin_config.disconnect_notice_mode_list
    err = None
    if "pushplus" in mode_list:
        err = await send_pushplus(bot_params, test=test)
    if "mail" in mode_list:
        err = await send_mail(bot_params, test=test)
    return err

async def send_pushplus(bot_params: BotParams, test: bool = False):
    """发送pushplus微信公众号通知"""
    global pushplus_config
    # 参数校验
    if not pushplus_config.check_params():
        error = "pushplus通知缺少配置参数，无法进行通知，\n" \
                "请参考https://github.com/Cypas/nonebot_plugin_disconnect_notice?tab=readme-ov-file#%EF%B8%8F-%E9%85%8D%E7%BD%AE" \
                "\n填写该推送方式配置项"
        logger.error(error)
        return error
    url = "http://www.pushplus.plus/send"
    if not test:
        title = f"[nonebot2]你的bot掉线了"
        content = f"你的 {bot_params.adapter_name} 适配器的bot账号: {bot_params.bot_id} 掉线了，可能是被风控了，赶快去看看吧"
    else:
        title = f"[nonebot2]掉线通知测试"
        content = f"这是一个掉线通知测试信息，你的bot并没有掉线"
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
    except (httpx.ConnectError,httpx.ConnectTimeout):
        err = f"pushplus通知失败，bot服务器网络错误"
        logger.error(err)
        return err
    except Exception as e:
        err = f"pushplus通知失败，错误信息如下{e}"
        logger.error(err)
        return err
    return

async def send_mail(bot_params: BotParams, test: bool = False):
    """发送邮件通知"""
    # 邮箱凭据
    global mail_config
    # 参数校验
    if not mail_config.check_params():
        error = "邮件通知缺少配置参数，无法进行通知，\n" \
                "请参考https://github.com/Cypas/nonebot_plugin_disconnect_notice?tab=readme-ov-file#%EF%B8%8F-%E9%85%8D%E7%BD%AE" \
                "\n填写该推送方式配置项"
        logger.error(error)
        return error
    # 邮件正文
    subject = f"[nonebot2]你的bot掉线了"
    content = f"你的 {bot_params.adapter_name} 适配器的bot账号: {bot_params.bot_id} 掉线了，可能是被风控了，赶快去看看吧"
    if test:
        subject = f"[nonebot2]掉线通知测试"
        content = f"这是一封掉线通知测试邮件，你的bot并没有掉线"

    # 构造邮件内容
    message = MIMEMultipart("alternative")
    message["Subject"] = Header(subject, 'utf-8')
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
        logger.error(f"邮件发送失败，错误信息如下{e}")
        return e
    logger.info("通知邮件发送成功!")
    return
