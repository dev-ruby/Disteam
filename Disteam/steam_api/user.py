from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from .player import PlayerServiceInterface

if TYPE_CHECKING:
    from .types.user import PlayerSummary as PlayerSummaryPayload
    from .requester import SteamApiRequester


class PlayerSummary:

    def __init__(self, *, data: PlayerSummaryPayload, requester: SteamApiRequester) -> None:
        self._requester = requester
        self._update(data)

        self.player_interface = PlayerServiceInterface(steam_id=self.id, requester=self._requester)

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
