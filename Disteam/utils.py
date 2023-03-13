import json

import requests

from typing import Dict, List
from constants import KEY, URLS


def makeUrl(url: str, /, **params: Dict[str, str]) -> str:
    query = [f"{key}={value}" for key, value in params.items()]

    if query:
        url += f"?{'&'.join(query)}" 

    return url


def getRecentGames(user_id: str, count: int = 3) -> List[Dict[str, str]]:
    url = makeUrl(
        URLS.RECENT_GAME,
        key=KEY,
        steamid=user_id,
        count=count,
    )
    response = requests.get(url)
    data = json.loads(response.text)
    return data["response"]["games"]


def getUserInfo(user_id: str) -> Dict[str, str]:
    url = makeUrl(
        URLS.USER_INFO,
        key=KEY,
        steamids=str([user_id]),
    )
    response = requests.get(url)
    data = json.loads(response.text)
    return data["response"]["players"][0]
