# pylint: disable=W0621
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path

from luoda.utils import flatten, lglobs

from .fixtures import tmpdir  # pylint: disable=W0611


def test_flatten() -> None:
    assert list(flatten([["a", "b"], [1, 2]])) == ["a", "b", 1, 2]
    assert list(flatten([[["aaa", "bbb"]]])) == [["aaa", "bbb"]]


def test_lglobs(tmpdir: Path) -> None:
    xs = ["foo.py", "bar.py", "qux.py", "bar.md", "qux.rst", "quux.md"]
    for x in xs:
        (tmpdir / x).touch()

    assert list(lglobs(["*.py"])) == [
        Path(p) for p in ["foo.py", "bar.py", "qux.py"]
    ]

    assert list(lglobs(["*.md", "*.rst"])) == [
        Path(p) for p in ["quux.md", "bar.md", "qux.rst"]
    ]
