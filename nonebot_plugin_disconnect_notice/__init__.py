import json
from datetime import datetime as dt, timedelta

from nonebot.internal.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot import Bot, require, get_bots, on_notice
from nonebot import logger

# onebot11 协议
from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.adapters.onebot.v11 import Event as V11Event
from nonebot import on_command
from nonebot.permission import SUPERUSER

from .config import driver, plugin_config, global_config, Config
from .dataClass import BotParams
from .notice import send_notice, mail_config, send_mail, server_config, pushplus_config
from .utils import PLATFORM_SERVER, PLATFORM_MAIL, PLATFORM_PUSHPLUS,PLATFORM_PUSHOVER

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

__plugin_meta__ = PluginMetadata(
    name="bot断连通知",
    description="bot断连时的通知插件，当前支持邮件通知，pushplus微信公众号通知，server酱公众号通知，pushover多平台设备通知",
    usage="""
    超级用户指令:
        /掉线测试:主动触发掉线通知测试
    """,
    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。
    homepage="https://github.com/Cypas/nonebot_plugin_disconnect_notice",
    # 发布必填。
    config=Config,
    supported_adapters=None,
)

notice_test = on_command("断连通知测试",aliases={"掉线测试","掉线通知测试"}, priority=8, block=True, permission=SUPERUSER)


@notice_test.handle()
async def _(matcher: Matcher):
    """主动触发掉线通知测试"""
    msg = "已发送测试通知\n"
    mode_list = plugin_config.disconnect_notice_mode_list
    if PLATFORM_MAIL in mode_list:
        msg += "\n当前通知渠道包括mail，若邮件未收到时请检查邮件垃圾箱"
    if PLATFORM_PUSHOVER in mode_list:
        msg += "\n当前通知渠道包括pushover，若未收到通知时，请检查是否有任一平台(安卓/ios/ipad/pc/mac)的app保持了后台运行且打开了系统通知"
    bot_params = BotParams(
        adapter_name="114514",
        bot_id="114514"
    )
    res = await send_notice(bot_params, test=True)
    if res is not None:
        msg = f"测试通知发送失败，请重新检查配置项参数正确性，错误信息为: {res}"
    await matcher.finish(msg)

# NapCatQQ与Lagrange.Core下线情况单独处理
offline = on_notice(priority=1, block=False)
@offline.handle()
async def _(bot: V11Bot,event: V11Event):
    if event.get_event_name() == "notice.bot_offline":
        des = json.loads(event.get_event_description().replace("'", '"'))
        if des:
            # 开发者模式下不生效
            platform = "NapCatQQ或Lagrange"
            bot_id = bot.self_id
            if not plugin_config.disconnect_notice_dev_mode:
                job_id = f"disconnect_notice_{platform}_{bot_id}"
                if scheduler.get_job(job_id):
                    scheduler.remove_job(job_id)
                # 计算运行时间
                run_time = dt.now() + timedelta(seconds=plugin_config.disconnect_notice_max_grace_time)

                bot_params = BotParams(
                    adapter_name=platform,
                    bot_id=bot_id,
                    tag = des['tag'],
                )
                scheduler.add_job(
                    id=job_id, func=cron_send_notice, args=[bot_params],
                    misfire_grace_time=60, coalesce=True, max_instances=1, trigger='date', run_date=run_time
                )
            else:
                logger.info(f"当前掉线通知已开启dev模式，不会进行任何实际通知")


@driver.on_bot_disconnect
async def disconnect(bot: Bot):
    """bot断连触发器"""
    # 开发者模式下不生效
    platform = bot.adapter.get_name()
    bot_id = bot.self_id
    if not plugin_config.disconnect_notice_dev_mode:
        job_id = f"disconnect_notice_{platform}_{bot_id}"
        if scheduler.get_job(job_id):
            scheduler.remove_job(job_id)
        # 计算运行时间
        run_time = dt.now() + timedelta(seconds=plugin_config.disconnect_notice_max_grace_time)

        bot_params = BotParams(
            adapter_name=platform,
            bot_id=bot_id
        )
        scheduler.add_job(
            id=job_id, func=cron_send_notice, args=[bot_params],
            misfire_grace_time=60, coalesce=True, max_instances=1, trigger='date', run_date=run_time
        )
    else:
        logger.info(f"当前掉线通知已开启dev模式，不会进行任何实际通知")

async def cron_send_notice(bot_params: BotParams):
    """定时任务：发送通知"""
    platform =bot_params.adapter_name
    bot_id = bot_params.bot_id
    # 重新检查bot是否接入
    bots = get_bots()
    bot = bots.get(bot_id)
    if (not bot) or (platform == "NapCatQQ或Lagrange"):
        logger.warning(f"平台:{platform} bot_id:{bot_id} 已掉线，即将进行通知")
        await send_notice(bot_params)
    else:
        logger.info(f"平台:{platform} bot_id:{bot_id} 已重连，无需进行通知")


@driver.on_bot_connect
async def connect(bot: Bot):
    """bot接入时检测配置完整性"""
    if isinstance(bot, V11Bot):
        mode_list = plugin_config.disconnect_notice_mode_list
        mode_name = ""
        params_ok = False
        if PLATFORM_PUSHPLUS in mode_list:
            mode_name = PLATFORM_PUSHPLUS
            params_ok = pushplus_config.check_params()
        if PLATFORM_MAIL in mode_list:
            mode_name = PLATFORM_MAIL
            params_ok = mail_config.check_params()
        if PLATFORM_SERVER in mode_list:
            mode_name = PLATFORM_SERVER
            params_ok = server_config.check_params()
        if PLATFORM_PUSHOVER in mode_list:
            mode_name = PLATFORM_PUSHOVER
            params_ok = server_config.check_params()
        if not params_ok:
            # 缺少参数,私聊通知主人
            super_user: str = list(global_config.superusers)[0]
            if super_user:
                msg = f"【插件nonebot-plugin-disconnect-notice】\n缺少{mode_name}配置项，请按照" \
                      "https://github.com/Cypas/nonebot_plugin_disconnect_notice#%EF%B8%8F-%E9%85%8D%E7%BD%AE" \
                      "\n添加配置项后，再重新载入插件"
                await bot.send_private_msg(user_id=int(super_user), message=msg)
