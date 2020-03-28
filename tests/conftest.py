from io import StringIO
from typing import Iterator, Optional

import py.code
import py.path
import pytest
import ruamel.yaml
from pytest import Collector

import clean_actions

yaml = ruamel.yaml.YAML()


def pytest_collect_file(
    path: py.path.local, parent: Collector
) -> Optional["YamlTestCaseFile"]:
    if path.basename.endswith(".case.yml"):
        return YamlTestCaseFile.from_parent(parent, fspath=path)
    return None


class YamlTestCaseFile(pytest.File):
    def collect(self) -> Iterator["YamlTestCaseItem"]:
        documents = yaml.load_all(self.fspath.open())
        for document in documents:
            yield YamlTestCaseItem.from_parent(
                self, name=document["it"], document=document, fspath=self.fspath
            )


class YamlTestCaseItem(pytest.Item):
    def __init__(self, name: str, parent: YamlTestCaseFile, document, fspath):
        self.validate_document(document)

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

    @classmethod
    def validate_document(cls, document):
        document_keys = list(document.keys())
        assert "it" in document_keys, "Missing 'it' statement in document"
        assert "given" in document_keys, "Missing 'given' statement in document"
        assert "expect" in document_keys, "Missing 'expect' statement in document"

    def get_given_contents(self) -> str:
        given_io = StringIO()
        yaml.dump(self.document["given"], given_io)
        return given_io.getvalue()

    def get_expect_contents(self) -> str:
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
