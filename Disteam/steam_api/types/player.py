from typing import List, TypedDict


class RecentGame(TypedDict):
    appid: str
    playtime_forever: int
    playtime_2weeks: int


class RecentGames(TypedDict):
    games: List[RecentGame]


class PlayerRecentGamesResponse(TypedDict):
    response: RecentGames
