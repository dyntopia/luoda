# pylint: disable=W0621
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path

from luoda.item import Item
from luoda.plugins.highlight import available, run

from ..fixtures import tmpdir  # pylint: disable=W0611


def test_available() -> None:
    assert available()


def test_run(tmpdir: Path) -> None:
    config = {
        "build": {
            "build-dir": tmpdir / "build",
            "highlight": "default",
        }
    }
    item = Item(path=Path(tmpdir / "xyz"))
    output = tmpdir / "build" / "static" / "highlight.css"

    assert run(item, config) == item
    assert output.is_file()
    assert output.read_text().count("color") > 0
