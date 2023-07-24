from typing import Union

from nonebot.internal.matcher import Matcher
from nonebot.plugin import PluginMetadata

# onebot11 协议
from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot import on_command
from nonebot.permission import SUPERUSER

from .config import driver, plugin_config, global_config
from .utils import send_notice, mail_config, send_mail

__plugin_meta__ = PluginMetadata(
    name="QQbot断连通知",
    description="QQbot断连时的通知插件",
    usage="""
    超级用户指令:
        断连通知测试:主动触发掉线通知测试
    """,
    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。
    homepage="https://github.com/Cypas/nonebot_plugin_disconnect_notice",
    # 发布必填。
    supported_adapters={"~onebot.v11"},
)

notice_test = on_command("断连通知测试", permission=SUPERUSER)


@notice_test.handle()
async def _(matcher: Matcher):
    """主动触发掉线通知测试"""
    msg = "已发送测试邮件，如未收到请检查邮件垃圾箱"
    res = send_mail("114514", test=True)
    if res is not None:
        msg = f"测试邮件发送失败，请重新检查配置项参数正确性，错误信息为: {res}"
    await matcher.finish(msg)


@driver.on_bot_disconnect
async def disconnect(bot: Union[V11Bot]):
    """bot断连触发器"""
    # 开发者模式下不生效
    if not plugin_config.disconnect_notice_dev_mode:
        send_notice(bot)


@driver.on_bot_connect
async def connect(bot: V11Bot):
    """bot接入时检测配置完整性"""
    if not mail_config.check_params():
        # 缺少参数,私聊通知主人
        super_user: str = list(global_config.superusers)[0]
        if super_user:
            await bot.send_private_msg(user_id=int(super_user), message="【插件nonebot-plugin-disconnect-notice】\n"
                                                                        "缺少mail配置项，请按照https://github.com"
                                                                        "/Cypas/nonebot_plugin_disconnect_notice#%EF%B8%8F-%E9%85%8D%E7%BD%AE"
                                                                        "\n添加配置项后，再重新载入插件")
