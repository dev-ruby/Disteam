import discord
import json
import requests
import re
from typing import Dict, List, Union
from constants import KEY, URLS


def makeUrl(url: str, /, **params: Dict[str, str]) -> str:
    query = [f"{key}={value}" for key, value in params.items()]

    if query:
        url += f"?{'&'.join(query)}"

    return url


def isUrl(url: str) -> bool:
    url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"

    return not (re.match(url_pattern, url) == None)


def getErrorEmbed(desc: str) -> discord.Embed:
    return discord.Embed(
        title=":no_entry: Error",
        description=desc,
        color=0xFF0000,
    )


def getRecentGames(user_id: str, count: int = 3) -> Union[List[Dict[str, str]], int]:
    url = makeUrl(
        URLS.RECENT_GAME,
        key=KEY,
        steamid=user_id,
        count=count,
    )
    response = requests.get(url)
    data = json.loads(response.text)

    if data["response"].get("games") == None:
        return 0

    return data["response"]["games"]


def getUserInfo(user_id: str) -> Union[Dict[str, str], int]:
    url = makeUrl(
        URLS.USER_INFO,
        key=KEY,
        steamids=str([user_id]),
    )
    response = requests.get(url)
    data = json.loads(response.text)

    if len(data["response"]["players"]) == 0:
        return 0

    return data["response"]["players"][0]


def getSteamIDbyURL(profile_url: str) -> Union[int, None]:
    if profile_url.startswith("https://steamcommunity.com/profiles/"):
        return profile_url.split("/")[-1]

    customurl = profile_url.split("/")[-1]
    url = makeUrl(URLS.CUSTOM_URL, key=KEY, vanityurl=customurl)
    response = requests.get(url)
    data = json.loads(response.text)

    if data["response"]["success"] == 42:
        return

    return data["response"]["steamid"]


def getUserLevel(user_id: str) -> Union[str, int]:
    url = makeUrl(URLS.USER_LEVEL, key=KEY, steamid=user_id)
    response = requests.get(url)

    if response.status_code == 500:
        return 0  # incorrect steam id

    data = json.loads(response.text)

    if data["response"] == {}:
        return 1  # private profile

    return str(data["response"]["player_level"])


def getUserOwnedGameCount(user_id: str) -> Union[str, int]:
    url = makeUrl(URLS.OWNED_GAMES, key=KEY, steamid=user_id)
    response = requests.get(url)

    if response.status_code == 500:
        return 0  # incorrect steam id

    data = json.loads(response.text)

    if data["response"] == {}:
        return 1  # private profile

    return str(data["response"]["game_count"])
