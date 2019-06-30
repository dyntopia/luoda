# pylint: disable=W0621
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from os import mkdir
from pathlib import Path

from pytest import raises

from luoda.config import ConfigError, read

from .fixtures import tmpdir  # pylint: disable=W0611


def test_missing_build(tmpdir: Path) -> None:
    config = tmpdir / "config"
    config.write_text(
        """
        [[collections]]
        name = "foo"
        template = "bar"
        paths = ["baz"]
        """
    )
    mkdir("collections")
    mkdir("templates")

    res = read(config)
    keys = len(res["build"].keys())
    assert keys > 0


def test_invalid_type(tmpdir: Path) -> None:
    config = tmpdir / "config"
    config.write_text(
        """
        [build]
        collection-dir = "c"
        template-dir = "t"
        [collections]
        """
    )
    mkdir("c")
    mkdir("t")

    with raises(ConfigError, match="expected a list: collections"):
        read(config)


def test_invalid_build_dir(tmpdir: Path) -> None:
    config = tmpdir / "config"
    config.write_text(
        """
        [build]
        collection-dir = "c"
        template-dir = "t"
        build-dir = 1234
        [[collections]]
        template = "foo"
        name = "bar"
        paths = []
        """
    )
    mkdir("c")
    mkdir("t")

    with raises(ConfigError, match="expected a directory: build.build-dir"):
        read(config)


def test_invalid_highlight(tmpdir: Path) -> None:
    config = tmpdir / "config"
    config.write_text(
        """
        [build]
        highlight = "abcdefgh"
        collection-dir = "c"
        template-dir = "t"
        """
    )
    mkdir("t")
    mkdir("c")

    with raises(ConfigError, match="expected a pygments style"):
        read(config)


def test_extra(tmpdir: Path) -> None:
    config = tmpdir / "config"
    config.write_text(
        """
        [build]
        collection-dir = "c"
        template-dir = "t"

        [extra]
        abc = 123
        xyz = "foo"
        """
    )
    mkdir("c")
    mkdir("t")

    res = read(config)
    assert res["extra"]["abc"] == 123
    assert res["extra"]["xyz"] == "foo"
