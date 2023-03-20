import re


class URI:
    __uri: str

    def __init__(self, url: str, args: dict[str, str] | None = None) -> None:
        if args:
            first: bool = True
            for key, val in args:
                url += "%s%s=%s" % ("?" if first else "&", key, val)
                first = False

        self.__uri = url

    def is_valid(self) -> bool:
        regex: str = "/^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$/"
        return re.match(regex, URI) != None

    def to_string(self) -> str:
        return self.__uri
