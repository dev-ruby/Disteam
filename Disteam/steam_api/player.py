from __future__ import annotations

from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .types.player import RecentGame as RecentGamePayload
    from .requester import SteamApiRequester

__all__ = (
    'PlayerServiceInterface',
    'RecentGame',
)


class RecentGame:

    def __init__(self, *, data: RecentGamePayload) -> None:
        self.id = data['appid']
        self._update(data)

    def _update(self, data: RecentGamePayload) -> None:
        self.playtime_forever: int = data['playtime_forever']
        self.playtime_2weeks: int = data['playtime_2weeks']


class PlayerServiceInterface:

    def __init__(self, *, steam_id: str, requester: SteamApiRequester) -> None:
        self.steam_id: str = steam_id
        self._requester: SteamApiRequester = requester

    async def fetch_level(self) -> int:
        level = await self._requester.get_steam_level(self.steam_id)
        return int(level['response']['player_level'])

    async def fetch_owned_games(self, include_appinfo: bool = False, include_free_games: bool = True) -> Dict:
        games = await self._requester.get_owned_games(
            self.steam_id,
            include_appinfo=include_appinfo,
            include_played_free_games=include_free_games,
        )
        return games

    async def fetch_recent_played_games(self, count: int = 3) -> List[RecentGame]:
        payload = await self._requester.get_recently_played_games(self.steam_id, count=count)
        games = payload['response']['games']
        return [RecentGame(data=game) for game in games]
