import requests
import json
import typing
from constants import KEY, URLS


def makeUrl(url: str, params: dict = {}) -> str:
    url_with_params = url
    if len(params) == 0:
        return url
    else:
        url_with_params += "?"
        for item in params.items():
            url_with_params += f"{item[0]}={item[1]}&"
    return url_with_params[:-1]


def getRecentGames(user_id: str, count: int = 3) -> typing.List[typing.Dict[str, str]]:
    url = makeUrl(
        URLS.RECENT_GAME,
        params={"key": KEY, "steamid": user_id, "count": count},
    )
    response = requests.get(url=url)
    if not (response.status_code == 200):
        return

    data = json.loads(response.text)
    return data["response"]["games"]


def getUserInfo(user_id: str) -> typing.Dict[str, str]:
    url = makeUrl(
        URLS.USER_INFO,
        params={"key": KEY, "steamids": [user_id]},
    )
    response = requests.get(url=url)
    if not (response.status_code == 200):
        return

    data = json.loads(response.text)
    return data["response"]["players"][0]
