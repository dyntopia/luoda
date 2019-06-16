# pylint: disable=C0102,W0212,W0621
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path
from textwrap import dedent
from typing import IO

from pytest import raises
from pytest_mock import MockFixture

from luoda import __project__
from luoda.config import read
from luoda.pipeline import Pipeline, PipelineError, build

from .fixtures import tmpdir, tmpfile  # pylint: disable=W0611


def test_unknown_plugins(tmpfile: IO[str]) -> None:
    tmpfile.write(
        """
        [build]
        plugins = ["foo", "bar"]
        [site]
        name = "m00"
        [[collections]]
        name = "abc"
        template = "xyz"
        paths = []
        """
    )
    tmpfile.seek(0)

    with raises(PipelineError, match=r"unknown plugin\(s\)"):
        build(read(tmpfile))


def test_plugins(tmpdir: Path) -> None:
    foo = dedent(
        """
        def available():
            return True

        def run(state):
            return state * 3
        """
    )
    (tmpdir / "foo.py").write_text(foo)

    bar = dedent(
        """
        def available():
            return False
        """
    )
    (tmpdir / "bar.py").write_text(bar)

    baz = dedent(
        """
        def available():
            return True

        def run(state):
            return state + 5
        """
    )
    (tmpdir / "baz.py").write_text(baz)

    pipeline = Pipeline("abc", ["."])
    pipeline.load(["foo", "bar", "baz"])

    assert [p.__file__ for p in pipeline._plugins] == ["./foo.py", "./baz.py"]
    assert pipeline.run(2) == 11


def test_unknown_run(tmpfile: IO[str], mocker: MockFixture) -> None:
    tmpfile.write(
        """
        [build]
        plugins = []
        [site]
        name = "m00"
        [[collections]]
        name = "abc"
        template = "xyz"
        paths = []
        """
    )
    tmpfile.seek(0)

    run = mocker.patch("luoda.pipeline.Pipeline.run")
    build(read(tmpfile))
    assert run.call_count == 1
