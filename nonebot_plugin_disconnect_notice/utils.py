import re

import httpx
from httpx import Response

HTTP_TIME_OUT = 10 # 请求超时，秒

PLATFORM_PUSHPLUS = "pushplus"
PLATFORM_MAIL = "mail"
PLATFORM_SERVER = "server"
PLATFORM_SERVER3 = "server3"
PLATFORM_PUSHOVER = "pushover"

class AsHttpReq(object):
    """httpx 异步请求封装"""

    @staticmethod
    async def get(url, **kwargs) -> Response:
        proxy = None
        async with httpx.AsyncClient(proxy=proxy) as client:
            response = await client.get(url, timeout=HTTP_TIME_OUT, **kwargs)
            return response

    @staticmethod
    async def post(url, **kwargs) -> Response:
        proxy = None
        async with httpx.AsyncClient(proxy=proxy) as client:
            response = await client.post(url, timeout=HTTP_TIME_OUT, **kwargs)
            return response


async def sc_send(sendkey, title, desp='', options=None):
    """发送消息，兼容Server酱Turbo和Server酱³"""
    if options is None:
        options = {}
    if sendkey.startswith('sctp'):
        # server3
        match = re.match(r'^sctp(\d+)t', sendkey)
        if match:
            url = f'https://{match.group(1)}.push.ft07.com/send/{sendkey}.send'
        else:
            raise ValueError("Invalid sendkey format for 'sctp'.")
    else:
        # server turbo
        url = f'https://sctapi.ftqq.com/{sendkey}.send'
    params = {
        'title': title,
        'desp': desp,
        **options
    }
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    response = await AsHttpReq.post(url, json=params, headers=headers)
    return response