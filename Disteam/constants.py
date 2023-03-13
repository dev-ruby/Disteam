import os

TOKEN = os.getenv("TOKEN")
KEY = os.getenv("KEY")


class EMOJIS:
    LOADING = "<a:Loading:1074281136924135485>"


class URLS:
    RECENT_GAME = "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/"
    USER_INFO = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    CUSTOM_URL = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
    USER_LEVEL = "https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/"
    OWNED_GAMES = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
