import json
import re
from constants import KEY, URLS
from typing import Union

import requests_async
from steam_game import SteamGame
from steam_profile import SteamProfile
from uri import URI


class SteamUser:
    pass


class SteamUser:
    __user_id: str
    __api_key: str

    @staticmethod
    async def query_user_async(uri: URI) -> Union[SteamUser, None]:
        __user_id: str | None
        __api_key: str = KEY

        url: str = uri.to_string()
        regex: str = "((https://)|(http://)|())steamcommunity.com/profiles/"
        if re.match(regex, url) != None:
            __user_id = url.split("/")[-1]
        else:
            req: URI = URI(
                URLS.CUSTOM_URL, {"key": __api_key, "vanityurl": url.split("/")[-1]}
            )
            res: str = await requests_async.get(req)
            dat = json.loads(res.text)
            __user_id = (
                None if dat["response"]["success"] == 42 else dat["response"]["steamid"]
            )

        return SteamUser(__user_id) if __user_id != None else None

    def __init__(self, id: str) -> None:
        self.__user_id = id
        self.__api_key = KEY

    @property
    def id(self) -> str:
        return self.__user_id

    def get_profile_uri(self) -> URI:
        return URI("https://steamcommunity.com/profiles/%s" % (self.__user_id))

    async def get_profile_async(self) -> SteamProfile | None:
        req: URI = URI(
            URLS.USER_INFO, {"key": self.__api_key, "steamids": self.__user_id}
        )
        res: str = await requests_async.get(req.to_string())
        dat = json.loads(res.text)

        if len(dat["response"]["players"]) == 0:
            return None

        return SteamProfile(dat["response"]["players"][0])

    async def get_level_async(self) -> str | None:
        req: URI = URI(
            URLS.USER_LEVEL, {"key": self.__api_key, "steamid": self.__user_id}
        )
        res: str = await requests_async.get(req.to_string())
        if res.status_code == 500:  # invalid response code
            return None

        dat = json.loads(res.text)
        if dat["response"] == {}:  # private profile
            return None

        return str(dat["response"]["player_level"])

    async def get_owned_game_count_async(self) -> int | None:
        req: URI = URI(
            URLS.OWNED_GAMES, {"key": self.__api_key, "steamid": self.__user_id}
        )
        res: str = await requests_async.get(req.to_string())
        if res.status_code == 500:  # invalid response code
            return None

        dat = json.loads(res.text)
        if dat["response"] == {}:
            return None

        return int(dat["response"]["game_count"])

    async def get_recent_games_async(self, count: int | None = 3) -> list[SteamGame]:
        req: URI = URI(
            URLS.RECENT_GAME,
            {"key": self.__api_key, "steamid": self.__user_id, "count": count},
        )
        res: str = await requests_async.get(req.to_string())
        dat: any = json.loads(res)

        games: list[SteamGame] = list()
        games_raw: list[dict[str, str]] = dat["response"].get("games")
        for game in games_raw:
            games.append(game)

        return games
