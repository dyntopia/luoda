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


def test_missing_required(tmpdir: Path) -> None:
    config = tmpdir / "config"
    config.write_text(
        """
        [site]
        [[collections]]
        name = "foo"
        template = "bar"
        paths = ["baz"]
        """
    )

    with raises(ConfigError, match="required key not provided: build"):
        read(config)


def test_invalid_type(tmpdir: Path) -> None:
    config = tmpdir / "config"
    config.write_text(
        """
        [build]
        template-dir = "t"
        [collections]
        [site]
        """
    )
    mkdir("t")

    with raises(ConfigError, match="expected a list: collections"):
        read(config)


def test_invalid_build_dir(tmpdir: Path) -> None:
    config = tmpdir / "config"
    config.write_text(
        """
        [build]
        template-dir = "t"
        build-dir = 1234
        [[collections]]
        template = "foo"
        name = "bar"
        paths = []
        [site]
        """
    )
    mkdir("t")

    with raises(ConfigError, match="expected a directory: build.build-dir"):
        read(config)
