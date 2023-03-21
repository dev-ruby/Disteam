import aiohttp
from typing import Tuple

from uri import URI


async def get(uri: URI) -> Tuple[str, int]:
    async with aiohttp.ClientSession() as session:
        async with session.get(str(uri), headers={"User-Agent" : "Mozilla/5.0"}) as response:
            return (await response.text(), response.status)
