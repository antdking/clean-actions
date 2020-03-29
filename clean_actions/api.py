from . import clean, yaml
from .features import (
    cleanup_commands,
    commands,
    global_run_as,
    strip_x_prefixed_root_tags,
)

_features = [
    global_run_as,
    commands,
    # These should go last, in case any other feature wants them.
    cleanup_commands,
    strip_x_prefixed_root_tags,
]


def process(contents: str) -> str:
    obj = yaml.load(contents)

    # Do processing
    for feature in _features:
        feature.execute(obj)

    clean.strip_known_invalid_tags(obj)
    return yaml.dump(obj)
