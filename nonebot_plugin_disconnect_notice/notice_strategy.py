from abc import ABC, abstractmethod
from typing import Optional
from nonebot import logger


class NoticeStrategy(ABC):
    """通知策略的抽象基类"""

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def check_params(self) -> bool:
        """检查参数是否填写完整"""
        pass

    @abstractmethod
    async def send(self, title: str, content: str) -> Optional[str]:
        """发送通知
        Returns:
            Optional[str]: 发送失败时返回错误信息,成功返回None
        """
        pass

    def get_platform_name(self) -> str:
        """获取平台名称"""
        return self.__class__.__name__.replace("Strategy", "").lower()

    async def send_with_check(self, title: str, content: str) -> Optional[str]:
        """发送通知(带参数检查)"""
        if not self.check_params():
            err = f"{self.get_platform_name()} 平台通知缺少配置参数,无法进行通知,\n" \
                  "请参考https://github.com/Cypas/nonebot_plugin_disconnect_notice#%EF%B8%8F-%E9%85%8D%E7%BD%AE\n" \
                  "填写该推送方式配置项"
            logger.error(err)
            return err

        return await self.send(title, content)
