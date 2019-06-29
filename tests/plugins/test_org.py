# pylint: disable=W0621
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path
from subprocess import CalledProcessError
from textwrap import dedent

from pytest import raises
from pytest_mock import MockFixture

from luoda.item import Item
from luoda.plugins._exceptions import PluginError
from luoda.plugins.org import available, parse_date, run

from ..fixtures import tmpdir  # pylint: disable=W0611


def test_available(mocker: MockFixture) -> None:
    which = mocker.patch("luoda.plugins.org.which")

    which.return_value = "xyz"
    assert available()

    which.return_value = None
    assert not available()


def test_parse_date() -> None:
    assert parse_date("1970-01-02") == 86400.0

    with raises(PluginError):
        parse_date("1970")


def test_run_not_org(tmpdir: Path) -> None:
    path = tmpdir / "abcd"
    path.touch()

    item = Item(path=path)
    assert run(item) == item


def test_run_invalid_process(tmpdir: Path, mocker: MockFixture) -> None:
    check_output = mocker.patch("luoda.plugins.org.check_output")
    check_output.side_effect = CalledProcessError(
        cmd=["foo"],
        output=b"bar",
        returncode=1,
    )

    with raises(PluginError, match="bar"):
        run(Item(path=tmpdir / "foo.org"))


def test_run_with_options(tmpdir: Path) -> None:
    org = dedent(
        """
        #+author: Foo Bar
        #+title: option title
        #+date: 1970-01-02

        *   first
        **  second
        text123

        #+begin_src python
        print("m00")
        #+end_src

        #+begin_src c
        exit(0);
        #+end_src

        #+begin_src foobarbazqux
        unknown lexer
        #+end_src

        #+begin_src
        no lang
        #+end_src
        """
    )
    (tmpdir / "xyz.org").write_text(org)
    item = run(Item(path=tmpdir / "xyz.org"))

    assert item.author == "Foo Bar"
    assert item.title == "option title"
    assert item.date == 86400.0
    assert item.content.count("option title") == 0
    assert item.content.count("first") == 1
    assert item.content.count("second") == 1
    assert item.content.count("text123") == 1
    assert item.content.count("unknown lexer") == 1
    assert item.content.count("no lang") == 1
    assert item.content.count("highlight") == 2


def test_run_without_options(tmpdir: Path) -> None:
    org = dedent(
        """
        *   first
        **  second
        text123
        """
    )
    (tmpdir / "xyz.org").write_text(org)
    item = run(Item(path=tmpdir / "xyz.org"))

    assert item.title == ""
    assert item.author == ""
    assert item.date == 0.0
    assert item.content.count("first") == 1
    assert item.content.count("second") == 1
    assert item.content.count("text123") == 1
