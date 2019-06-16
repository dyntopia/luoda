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

    got = sorted([p.name for p in lglobs(tmpdir, ["*.py"], [])])
    want = sorted(["foo.py", "bar.py", "qux.py"])
    assert got == want

    got = sorted([p.name for p in lglobs(tmpdir, ["*.md", "*.rst"], [])])
    want = sorted(["quux.md", "bar.md", "qux.rst"])
    assert got == want

    got = sorted([p.name for p in lglobs(tmpdir, ["*.md", "*rst"], ["b*.md"])])
    want = sorted(["quux.md", "qux.rst"])
    assert got == want
