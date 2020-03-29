import re

_known_invalid_keywords = [
    "commands",
    "runs-on",
]
_known_invalid_patterns = [
    re.compile("x-.*"),
]


def strip_known_invalid_tags(obj: dict) -> None:
    for keyword in _known_invalid_keywords:
        obj.pop(keyword, None)
    for key in list(obj.keys()):
        for pattern in _known_invalid_patterns:
            if pattern.match(key):
                obj.pop(key)
                break
