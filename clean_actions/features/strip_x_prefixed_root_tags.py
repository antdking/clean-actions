import re

_x_prefix_pattern = re.compile(r"[xX]-.*")


def execute(obj: dict) -> None:
    for key in list(obj.keys()):
        if _x_prefix_pattern.match(key):
            obj.pop(key)
