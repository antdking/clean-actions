from . import clean, yaml
from .features import global_run_as

_features = [
    global_run_as,
]


def process(contents: str) -> str:
    obj = yaml.load(contents)

    # Do processing
    for feature in _features:
        feature.execute(obj)

    clean.strip_known_invalid_tags(obj)
    return yaml.dump(obj)
