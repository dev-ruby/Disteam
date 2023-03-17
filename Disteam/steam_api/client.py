import asyncio

from typing import List

from .requester import SteamApiRequester

from .user import PlayerSummary

__all__ = (
    'SteamApiClient',
)


class SteamApiClient:

    def __init__(self, key: str) -> None:
        self.loop = asyncio.get_event_loop()
        self.key = key
        self.requester = SteamApiRequester(self.loop, key=key)

    async def fetch_player(self, steam_id: str) -> PlayerSummary:
        users = await self.requester.get_player([steam_id])
        payloads = users['response']['players']

        if not payloads:
            raise Exception(f'User Id {steam_id} is not founded.')

        return PlayerSummary(data=payloads[0], requester=self.requester)

    async def fetch_players(self, steam_ids: List[str]) -> List[PlayerSummary]:
        users = await self.requester.get_player(steam_ids)
        payloads = users['response']['players']

        if not payloads:
            raise Exception('Any user not founded.')

        return [PlayerSummary(data=payload, requester=self.requester) for payload in payloads]

    async def fetch_player_level(self, steam_id: str) -> int:
        lvl = await self.requester.get_steam_level(steam_id)
        return int(lvl['response']['player_level'])
