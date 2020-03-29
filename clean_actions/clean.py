_known_invalid_keywords = [
    "commands",
]


def strip_known_invalid_tags(obj: dict) -> None:
    for keyword in _known_invalid_keywords:
        obj.pop(keyword, None)
