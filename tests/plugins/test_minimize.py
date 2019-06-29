# pylint: disable=W0621
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path

from luoda.item import Item
from luoda.plugins.minimize import available, run

from ..fixtures import tmpdir  # pylint: disable=W0611


def test_available() -> None:
    assert available()


def test_run(tmpdir: Path) -> None:
    tests = [
        ("", ""),
        ("<html>\n\n\n", "<html>"),
        ("<div>\n<p>\n\n\n foo \n\n\n</p></div>", "<div><p> foo </p></div>"),
        ("<p>\n\n abcd \n</p>", "<p> abcd </p>"),
        (b"<p>\n\n abcd \n</p>", b"<p>\n\n abcd \n</p>"),
    ]

    for a, b in tests:
        assert run(Item(path=tmpdir, content=a)).content == b  # type: ignore
