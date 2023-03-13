import os

TOKEN = os.getenv("TOKEN")
KEY = os.getenv("KEY")


class EMOJIS:
    LOADING = "<a:Loading:1074281136924135485>"


class URLS:
    RECENT_GAME = "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/"
    USER_INFO = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
