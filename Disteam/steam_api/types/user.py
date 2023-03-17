from typing import List, TypedDict


class PlayerSummary(TypedDict):
    steamid: str
    communityvisibilitystate: int
    profilestate: int
    personaname: str
    lastlogoff: int
    profileurl: str
    avatar: str
    avatarmedium: str
    avatarfull: str


class Players(TypedDict):
    players: List[PlayerSummary]


class PlayerSummaryResponse(TypedDict):
    response: Players
