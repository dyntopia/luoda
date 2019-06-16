# pylint: disable=W0621
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from typing import IO

from pytest import raises

from luoda.config import ConfigError, read

from .fixtures import tmpfile  # pylint: disable=W0611


def test_missing_required(tmpfile: IO[str]) -> None:
    tmpfile.write(
        """
        [site]
        [[collections]]
        name = "foo"
        template = "bar"
        paths = ["baz"]
        """
    )
    tmpfile.seek(0)

    with raises(ConfigError, match="required key not provided: build"):
        read(tmpfile)


def test_invalid_type(tmpfile: IO[str]) -> None:
    tmpfile.write(
        """
        [build]
        [collections]
        [site]
        """
    )
    tmpfile.seek(0)

    with raises(ConfigError, match="expected a list: collections"):
        read(tmpfile)
