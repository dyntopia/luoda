# pylint: disable=W0621
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path

from luoda.item import Item
from luoda.plugins.write import available, run

from ..fixtures import tmpdir  # pylint: disable=W0611


def test_available() -> None:
    assert available()


def test_run_relative(tmpdir: Path) -> None:
    files = [
        ("src/index.md", "dst/index.html"),
        ("src/foo.md", "dst/foo/index.html"),
        ("src/bar/index.md", "dst/bar/index.html"),
        ("src/bar/baz.md", "dst/bar/baz/index.html"),
        ("src/abc/def/index.md", "dst/abc/def/index.html"),
        ("src/abc/def/m00.md", "dst/abc/def/m00/index.html"),
    ]

    config = {
        "build": {
            "build-dir": Path("dst"),
            "collection-dir": Path("src"),
        }
    }

    config["build"]["build-dir"].mkdir(parents=True)
    config["build"]["collection-dir"].mkdir(parents=True)

    for src, _ in files:
        path = Path(src)
        item = Item(path=path, content=src)
        run(item, config=config)

    for src, dst in files:
        assert (tmpdir / dst).read_text() == src


def test_run_absolute(tmpdir: Path) -> None:
    files = [
        (tmpdir / "x/src/index.md", "dst/index.html"),
        (tmpdir / "x/src/foo.md", "dst/foo/index.html"),
        (tmpdir / "x/src/bar/index.md", "dst/bar/index.html"),
        (tmpdir / "x/src/bar/baz.md", "dst/bar/baz/index.html"),
        (tmpdir / "x/src/abc/def/index.md", "dst/abc/def/index.html"),
        (tmpdir / "x/src/abc/def/m00.md", "dst/abc/def/m00/index.html"),
    ]

    config = {
        "build": {
            "build-dir": Path("dst"),
            "collection-dir": tmpdir / "x" / Path("src"),
        }
    }

    config["build"]["build-dir"].mkdir(parents=True)
    config["build"]["collection-dir"].mkdir(parents=True)

    for src, _ in files:
        item = Item(path=src, content=str(src))
        run(item, config=config)

    for src, dst in files:
        assert (tmpdir / dst).read_text() == str(src)
