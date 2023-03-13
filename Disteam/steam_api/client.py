import asyncio

from typing import List

from .requester import SteamApiRequester

from .user import SteamUser

__all__ = (
    'SteamApiClient',
)


class SteamApiClient:

    def __init__(self, token: str) -> None:
        self.loop = asyncio.get_event_loop()
        self.token = token
        self.requester = SteamApiRequester(self.loop, token=token)

    async def fetch_user(self, user_id: str) -> SteamUser:
        users = await self.requester.get_users([user_id])
        payloads = users['response']['players']

        if not payloads:
            raise Exception(f'User Id {user_id} is not founded.')

        return SteamUser(data=payloads[0], requester=self.requester)

    async def fetch_users(self, user_ids: List[str]) -> List[SteamUser]:
        users = await self.requester.get_users(user_ids)
        payloads = users['response']['players']

        if not payloads:
            raise Exception('Any user not founded.')

        return [SteamUser(data=payload, requester=self.requester) for payload in payloads]

