from __future__ import annotations

import json
import aiohttp
import asyncio

from urllib.parse import quote as _uriquote
from typing import Any, Dict, ClassVar, Coroutine, Optional, Union, List, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .types.user import RawPlayerSummaries as PlayerSummariesPayload

    T = TypeVar('T')
    Response = Coroutine[Any, Any, T]


async def json_or_text(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text(encoding='utf-8')

    try:
        if response.headers['content-type'] == 'application/json':
            return json.loads(text)

    except KeyError:
        pass

    return text


class UrlRoute:
    BASE_URL: ClassVar[str] = 'https://api.steampowered.com'

    def __init__(self, method: str, path: str, **params: Any) -> None:
        self.path: str = path
        self.method: str = method
        url = self.BASE_URL + self.path

        if params:
            url = url.format_map({k: _uriquote(v) if isinstance(v, str) else v for k, v in params.items()})

        self.url = url


class SteamApiRequester:

    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        *,
        token: str,
    ) -> None:
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop() if loop is None else loop
        self.lock = asyncio.Lock()

        self.__session: Optional[aiohttp.ClientSession] = None
        self.__token: str = token

    async def request(
        self,
        route: UrlRoute,
        **kwargs: Any
    ) -> Any:
        method = route.method
        url = route.url

        with self.lock:

            if self.__session is None:
                self.__session = aiohttp.ClientSession()

            async with self.__session.request(method, url, **kwargs) as response:
                data = await json_or_text(response)

                if 300 > response.status >= 200:
                    return data

                raise Exception(f"Fail to request. Status: {response.status}")

    async def close(self) -> None:
        if not self.__session.closed:
            await self.__session.close()

    def get_users(self, user_ids: List[str]) -> Response[PlayerSummariesPayload]:
        r = UrlRoute('GET', '/ISteamUser/GetPlayerSummaries/v2/{user_ids}', user_ids=user_ids)
        return self.request(r)
