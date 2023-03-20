from datetime import datetime

from uri import URI

class SteamProfile:
    __persona_name: str
    __contry_code: str | None
    __created_time: datetime | None
    __thumbnail_url: URI
    
    def __init__(self, dat: dict[str,str]) -> None:
        epoch = dat.get("timecreated")
        lcid = dat.get("loccontrycode")
        
        self.__persona_name = dat["personaname"]
        self.__contry_code = lcid if lcid else None
        self.__created_time = datetime.utcfromtimestamp(dat.get("timecreated")) if epoch else None
        self.__thumbnail_url = URI(dat["avatarfull"])
        
    @property
    def persona_name(self) -> str:
        return self.__persona_name
    
    @property
    def contry_code(self) -> str | None:
        return self.__contry_code
    
    @property
    def created_time(self) -> datetime | None:
        return self.__created_time
    
    @property
    def thumbnail_url(self) -> URI:
        return self.__thumbnail_url