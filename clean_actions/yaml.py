import io
from typing import Iterable, cast

import ruamel.yaml


def _yaml(*, output: io.StringIO = None) -> ruamel.yaml.YAML:
    yaml = ruamel.yaml.YAML(output=output)

    yaml.preserve_quotes = True
    yaml.width = 100000000000

    # Strip out aliases + anchors when dumping
    yaml.constructor.flatten_mapping = _flatten_mapping(yaml.constructor)
    yaml.representer.ignore_aliases = lambda x: True
    return yaml


def _flatten_mapping(self):
    def inner(node: ruamel.yaml.nodes.MappingNode):
        ruamel.yaml.SafeConstructor.flatten_mapping(self, node)
        # we're not looking at a merged node
        if not getattr(node, "merge", None):
            return None

        merged = cast(list, node.merge)
        # ruamel prepends the value, so remove them
        original_value = node.value[len(merged) :]
        original_value_keys = [key.value for key, _ in original_value]

        # Add in the merge nodes, but only if they're not found on the original value.
        new_value = [
            (key, val) for key, val in merged if key.value not in original_value_keys
        ] + original_value

        node.value = new_value

        del node.merge  # We're manually merging, so don't let ruamel see this.
        return None

    return inner


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
