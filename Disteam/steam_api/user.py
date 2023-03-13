from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from .types.user import PlayerSummary

    from .requester import SteamApiRequester

__all__ = (
    'SteamUser',
)


class SteamUser:

    def __init__(self, *, data: PlayerSummary, requester: SteamApiRequester) -> None:
        self._requester = requester
        self._update(data)

    def __str__(self) -> str:
        return self.steam_id

    def _update(self, data: PlayerSummary) -> None:
        self.steam_id: str = data['steamid']
        self.community_visibility_state: int = data['communityvisibilitystate']
        self.profile_state: int = data['profilestate']
        self.name: str = data['personaname']
        self.profile_url: str = data['profileurl']
        self.avatar: str = data['avatar']

        self.last_logoff: datetime = datetime.fromtimestamp(data['lastlogoff'])
