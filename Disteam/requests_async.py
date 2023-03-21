import aiohttp
from typing import Tuple


async def get(url: str) -> Tuple[str, int]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"User-Agent" : "Mozilla/5.0"}) as response:
            return (await response.text(), response.status)
