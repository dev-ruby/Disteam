import aiohttp
from typing import Tuple


async def get(url: str) -> Tuple[str, int]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return (await response.text(), response.status)
