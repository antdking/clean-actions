from clean_actions import yaml


def test_can_load_a_yaml_document():
    input = "- {}"
    expected = [{}]
    actual = yaml.load(input)

    assert actual == expected


def test_can_load_multiple_yaml_documents():
    input = "\n".join(("---", "- {}", "---", "- {}"))

    expected = [[{}], [{}]]

    actual = list(yaml.load_all(input))

    assert actual == expected
