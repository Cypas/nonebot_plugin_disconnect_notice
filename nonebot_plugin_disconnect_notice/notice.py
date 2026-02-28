from nonebot import logger, Bot
from .config import plugin_config
from .dataClass import MailConfig, BotParams, PushPlusConfig, ServerConfig, PushOverConfig, Server3Config, FeiShuConfig
from .utils import *
from .strategies import (
    MailStrategy,
    PushPlusStrategy,
    ServerStrategy,
    Server3Strategy,
    PushOverStrategy,
    FeiShuStrategy
)

# 配置实例
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


class NoticeContext:
    """通知上下文,管理所有通知策略"""
    
    def __init__(self):
        self._strategies = {
            PLATFORM_MAIL: MailStrategy(mail_config),
            PLATFORM_PUSHPLUS: PushPlusStrategy(pushplus_config),
            PLATFORM_SERVER: ServerStrategy(server_config),
            PLATFORM_SERVER3: Server3Strategy(server3_config),
            PLATFORM_PUSHOVER: PushOverStrategy(pushover_config),
            PLATFORM_FEISHU: FeiShuStrategy(feishu_config),
        }
    
    def get_strategy(self, platform: str):
        """获取指定平台的通知策略"""
        return self._strategies.get(platform)
    
    def get_all_strategies(self):
        """获取所有通知策略"""
        return self._strategies


# 创建全局通知上下文实例
notice_context = NoticeContext()


async def send_notice(bot_params: BotParams, test=False):
    """整合发送通知消息"""
    mode_list = plugin_config.disconnect_notice_mode_list
    
    # 构建消息主体
    if not test:
        title = f"[nonebot2]你的bot掉线了"
        if not bot_params.tag:
            content = f"你的 {bot_params.adapter_name} 适配器的bot账号: {bot_params.bot_id} 掉线了，可能是被风控了，赶快去看看吧"
        else:
            content = f"你的 {bot_params.adapter_name} 适配器的bot账号: {bot_params.bot_id} 掉线了，原因为: {bot_params.tag} 。赶快去看看吧"
    else:
        title = f"[nonebot2]掉线通知测试"
        content = f"这是一个掉线通知测试信息，你的bot并没有掉线"
    
    # 使用策略模式发送通知
    last_error = None
    for platform in mode_list:
        strategy = notice_context.get_strategy(platform)
        if strategy:
            err = await strategy.send_with_check(title, content)
            if err:
                logger.error(err)
                last_error = err
    
    return last_error
