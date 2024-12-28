import httpx
from httpx import Response

HTTP_TIME_OUT = 10 # 请求超时，秒

PLATFORM_PUSHPLUS = "pushplus"
PLATFORM_MAIL = "mail"
PLATFORM_SERVER = "server"
PLATFORM_PUSHOVER = "pushover"

class AsHttpReq(object):
    """httpx 异步请求封装"""

    @staticmethod
    async def get(url, **kwargs) -> Response:
        proxies = None
        async with httpx.AsyncClient(proxies=proxies) as client:
            response = await client.get(url, timeout=HTTP_TIME_OUT, **kwargs)
            return response

    @staticmethod
    async def post(url, **kwargs) -> Response:
        proxies = None
        async with httpx.AsyncClient(proxies=proxies) as client:
            response = await client.post(url, timeout=HTTP_TIME_OUT, **kwargs)
            return response