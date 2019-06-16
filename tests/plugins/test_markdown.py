# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path

from luoda.item import Item
from luoda.plugins.markdown import available, run


def test_available() -> None:
    assert available()


def test_not_markdown() -> None:
    path = Path("foo")
    item = Item(path=path)

    assert run(item) == item


def test_no_title() -> None:
    path = Path("foo.md")
    path.write_text("## second")
    item = Item(path=path)

    res = run(item)
    assert res.content.index("second")
    assert res != item


def test_title() -> None:
    path = Path("foo.md")
    path.write_text("#  first \n ## second")
    item = Item(path=path)

    res = run(item)
    assert res.content.index("first")
    assert res.content.index("second")
    assert res.title == "first"
    assert res != item
