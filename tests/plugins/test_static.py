# pylint: disable=W0621
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path

from luoda.item import Item
from luoda.plugins.static import available, run

from ..fixtures import tmpdir  # pylint: disable=W0611


def test_run(tmpdir: Path) -> None:
    tests = [
        ("x.html", "template", False),
        ("x.html", "", True),
        ("xyz", "template", False),
        ("xyz", "", False),
    ]

    for name, template, supported in tests:
        (tmpdir / name).write_text(name)
        item = Item(path=tmpdir / name, template=template)
        if supported:
            assert run(item).content == name.encode()
        else:
            assert run(item) == item


def test_available() -> None:
    assert available()
