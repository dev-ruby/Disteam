from __future__ import annotations

import json
import aiohttp
import asyncio

from urllib.parse import quote as _uriquote
from typing import Any, Dict, ClassVar, Coroutine, Optional, Union, List, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .types.user import PlayerSummaryResponse as PlayerSummariesPayload
    from .types.player import PlayerRecentGamesResponse as PlayerRecentGamesPayload

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
        key: str,
    ) -> None:
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop() if loop is None else loop
        self.lock = asyncio.Lock()

        self.__session: Optional[aiohttp.ClientSession] = None
        self.__key: str = key

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

    def get_player(self, steam_ids: List[str]) -> Response[PlayerSummariesPayload]:
        r = UrlRoute(
            'GET',
            '/ISteamUser/GetPlayerSummaries/v2?steamids={steam_ids}&key={key}',
            steam_ids=steam_ids,
            key=self.__key,
        )
        return self.request(r)

    def get_steam_level(self, steam_id: str):
        r = UrlRoute(
            'GET',
            '/IPlayerService/GetSteamLevel/v1/steamdid={steam_id}&key={key}',
            steam_id=steam_id,
            key=self.__key,
        )
        return self.request(r)

    def get_owned_games(
        self,
        steam_id: str,
        include_appinfo: bool = False,
        include_played_free_games: bool = True,
    ):
        r = UrlRoute(
            'GET',
            '/IPlayerService/GetOwnedGames/v1/steamid={steam_id}&key={key}'
            '&include_appinfo={include_appinfo}&include_played_free_games={include_played_free_games}',
            steam_id=steam_id,
            include_appinfo=include_appinfo,
            include_played_free_games=include_played_free_games,
            key=self.__key,
        )
        return self.request(r)

    def get_recently_played_games(self, steam_id: str, count: int) -> Response[PlayerRecentGamesPayload]:
        r = UrlRoute(
            'GET',
            '/IPlayerService/GetRecentlyPlayedGames/v1/steamid={steam_id}&count={count}&key={key}',
            steam_id=steam_id,
            count=count,
            key=self.__key,
        )
        return self.request(r)
