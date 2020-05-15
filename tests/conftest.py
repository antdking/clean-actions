from io import StringIO
from typing import Iterator, Optional

import py.code
import py.path
import pytest
import ruamel.yaml
from pytest import Collector

import clean_actions

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True
yaml.width = 1000000000000


def pytest_collect_file(
    path: py.path.local, parent: Collector
) -> Optional["YamlTestCaseFile"]:
    if path.basename.endswith(".case.yml"):
        return YamlTestCaseFile.from_parent(parent, fspath=path)
    return None


class YamlTestCaseFile(pytest.File):
    def collect(self) -> Iterator["YamlTestCaseItem"]:
        documents = list(yaml.load_all(self.fspath.open()))
        for document in documents:
            self.validate_document(document)
            yield YamlTestCaseItem.from_parent(
                self, name=document["it"], document=document, fspath=self.fspath
            )

    @classmethod
    def validate_document(cls, document):
        document_keys = list(document.keys())
        line_number = document.lc.line
        errors = []
        if "it" not in document_keys:
            errors.append(f"Missing 'it' statement in document, line {line_number}")
        if "given" not in document_keys:
            errors.append(f"Missing 'given' statement in document, line {line_number}")
        if "expect" not in document_keys:
            errors.append(f"Missing 'expect' statement in document, line {line_number}")
        if errors:
            raise cls.CollectError("\n".join(errors))


class YamlTestCaseItem(pytest.Item):
    def __init__(self, name: str, parent: YamlTestCaseFile, document, fspath):
        super().__init__(name, parent)
        self.document = document
        self.fspath

    def runtest(self):
        given = self.get_given_contents()
        expected = self.get_expect_contents()

        actual = clean_actions.process(given)

        assert actual == expected, "Processed contents does not match expected workflow"

    @property
    def module(self):
        # Hack to make pytest-randomly work correctly
        return self.parent

    def get_given_contents(self) -> str:
        if isinstance(self.document["given"], str):
            return self.document["given"]
        given_io = StringIO()
        yaml.dump(self.document["given"], given_io)
        return given_io.getvalue()

    def get_expect_contents(self) -> str:
        if isinstance(self.document["expect"], str):
            return self.document["expect"]
        expect_io = StringIO()
        yaml.dump(self.document["expect"], expect_io)
        return expect_io.getvalue()

    def _prunetraceback(self, excinfo):
        if not self.config.getoption("fulltrace", False):
            tb = excinfo.traceback
            code = py.code.Code(self.runtest)
            path, firstlineno = code.path, code.firstlineno

            ptb = tb.cut(path=path, firstlineno=firstlineno)
            if tb == ptb:
                ptb = tb.cut(path=path)
            excinfo.traceback = ptb.filter()

    def reportinfo(self):
        return (self.fspath, None, self.get_domain())

    def get_domain(self):
        return "::".join([self.fspath.relto(py.path.local()), self.document["it"]])
