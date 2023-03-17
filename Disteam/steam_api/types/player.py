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


class RecentGame(TypedDict):
    appid: str
    playtime_forever: int
    playtime_2weeks: int


class RecentGames(TypedDict):
    games: List[RecentGame]


class PlayerRecentGamesResponse(TypedDict):
    response: RecentGames


class PlayerSummaryResponse(TypedDict):
    response: Players
