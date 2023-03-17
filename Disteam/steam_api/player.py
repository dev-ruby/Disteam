from __future__ import annotations

from datetime import datetime
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .types.player import PlayerSummary as PlayerSummaryPayload, RecentGame as RecentGamePayload
    from .requester import SteamApiRequester

__all__ = (
    'PlayerSummary',
    'RecentGame',
)


class RecentGame:

    def __init__(self, *, data: RecentGamePayload) -> None:
        self.id = data['appid']
        self._update(data)

    def _update(self, data: RecentGamePayload) -> None:
        self.playtime_forever: int = data['playtime_forever']
        self.playtime_2weeks: int = data['playtime_2weeks']


class PlayerSummary:

    def __init__(self, *, data: PlayerSummaryPayload, requester: SteamApiRequester) -> None:
        self._requester = requester
        self._update(data)

    def __str__(self) -> str:
        return self.id

    def _update(self, data: PlayerSummaryPayload) -> None:
        self.id: str = data['steamid']
        self.community_visibility_state: int = data['communityvisibilitystate']
        self.profile_state: int = data['profilestate']
        self.name: str = data['personaname']
        self.profile_url: str = data['profileurl']
        self.avatar: str = data['avatar']

        self.last_logoff: datetime = datetime.fromtimestamp(data['lastlogoff'])

    async def fetch_level(self) -> int:
        level = await self._requester.get_steam_level(self.id)
        return int(level['response']['player_level'])

    async def fetch_owned_games(self, include_appinfo: bool = False, include_free_games: bool = True) -> Dict:
        games = await self._requester.get_player_owned_games(
            self.id,
            include_appinfo=include_appinfo,
            include_played_free_games=include_free_games,
        )
        return games

    async def fetch_recent_played_games(self, count: int = 3) -> List[RecentGame]:
        payload = await self._requester.get_player_recently_games(self.id, count=count)
        games = payload['response']['games']
        return [RecentGame(data=game) for game in games]
