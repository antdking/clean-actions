from . import clean, yaml


def process(contents: str) -> str:
    obj = yaml.load(contents)

    # Do processing

    clean.strip_known_invalid_tags(obj)
    return yaml.dump(obj)
