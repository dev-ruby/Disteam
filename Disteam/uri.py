import re
from typing import Optional


class URI:
    __uri: str

    def __init__(self, url: str, args: Optional[dict[str, str]] = None) -> None:
        if args:
            first: bool = True
            for key, val in args.items():
                url += "%s%s=%s" % ("?" if first else "&", key, val)
                first = False

        self.__uri = url

    def is_valid(self) -> bool:
        url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"

        return not (re.match(url_pattern, str(self)) == None)

    def __str__(self) -> str:
        return self.__uri
