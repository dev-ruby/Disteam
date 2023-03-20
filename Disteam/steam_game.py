class Playtime:
    h: int
    m: int

    def __init__(self, h: int, m: int) -> None:
        self.h = h
        self.m = m


class SteamGame:
    __name: str
    __id: str
    __playtime: int
    __playtime_2weeks: int

    def __init__(self, dat: dict[str, str]) -> None:
        self.__name = dat["name"]
        self.__id = dat["appid"]
        self.__playtime = dat["playtime_forever"]
        self.__playtime_2weeks = dat["playtime_2weeks"]

    @property
    def name(self) -> str:
        return self.__name

    @property
    def id(self) -> str:
        return self.__id

    @property
    def playtime(self) -> Playtime:
        h, m = divmod(self.__playtime, 60)
        return Playtime(h, m)

    @property
    def playtime_2weeks(self) -> playtime:
        h, m = divmod(self.__playtime_2weeks, 60)
        return Playtime(h, m)
