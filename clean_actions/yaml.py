import io
from typing import Iterable

import ruamel.yaml


def _yaml(*, output: io.StringIO = None) -> ruamel.yaml.YAML:
    yaml = ruamel.yaml.YAML(output=output)

    # Strip out aliases + anchors when dumping
    yaml.representer.ignore_aliases = lambda x: True
    yaml.allow_duplicate_keys = True

    return yaml


def load(contents: str) -> dict:
    with _yaml() as yaml:
        return yaml.load(contents)


def load_all(contents: str) -> Iterable[dict]:
    with _yaml() as yaml:
        return yaml.load_all(contents)


def dump(obj: dict) -> str:
    target = io.StringIO()
    with _yaml(output=target) as yaml:
        yaml.dump(obj)
    return target.getvalue()
