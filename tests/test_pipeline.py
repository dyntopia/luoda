# pylint: disable=C0102,W0212,W0621
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from os import mkdir
from pathlib import Path
from textwrap import dedent

from pytest import raises
from pytest_mock import MockFixture

from luoda import __project__
from luoda.pipeline import Pipeline, PipelineError, build

from .fixtures import tmpdir  # pylint: disable=W0611


def test_unknown_plugins(tmpdir: Path) -> None:
    config = tmpdir / "config"
    config.write_text(
        """
        [build]
        collection-dir = "c"
        template-dir = "t"
        plugins = ["foo", "bar"]
        [site]
        name = "m00"
        [[collections]]
        name = "abc"
        template = "xyz"
        paths = []
        """
    )
    mkdir("c")
    mkdir("t")

    with raises(PipelineError, match=r"unknown plugin\(s\)"):
        build(config)


def test_ignored_plugins(tmpdir: Path) -> None:
    foo = dedent(
        """
        def available():
            return True

        def run(state):
            return state
        """
    )
    (tmpdir / "_foo.py").write_text(foo)

    pipeline = Pipeline("abc", ["."])

    with raises(PipelineError, match=r"unknown plugin"):
        pipeline.load(["_foo"])


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


def test_unknown_run(tmpdir: Path, mocker: MockFixture) -> None:
    config = tmpdir / "config"
    config.write_text(
        """
        [build]
        collection-dir = "c"
        template-dir = "t"
        plugins = []
        [site]
        name = "m00"
        [[collections]]
        name = "abc"
        template = "xyz"
        paths = ["*.md"]
        """
    )
    mkdir("c")
    mkdir("t")

    mds = ["foo.md", "bar.md", "baz.md"]
    for md in mds:
        (tmpdir / "c" / md).touch()

    run = mocker.patch("luoda.pipeline.Pipeline.run")
    build(config)

    assert run.call_count == len(mds)
