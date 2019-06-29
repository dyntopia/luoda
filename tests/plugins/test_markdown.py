# pylint: disable=W0621
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path
from textwrap import dedent

from luoda.item import Item
from luoda.plugins.markdown import available, run

from ..fixtures import tmpdir  # pylint: disable=W0611


def test_available() -> None:
    assert available()


def test_not_markdown() -> None:
    path = Path("foo")
    item = Item(path=path)

    assert run(item) == item


def test_no_title(tmpdir: Path) -> None:
    path = tmpdir / "foo.md"
    path.write_text("## second")
    item = Item(path=path)

    res = run(item)
    assert res.content.index("second")
    assert res != item


def test_title(tmpdir: Path) -> None:
    path = tmpdir / "foo.md"
    path.write_text("#  first \n ## second")
    item = Item(path=path)

    res = run(item)
    assert res.content.count("first") == 0
    assert res.content.count("second") == 1
    assert res.title == "first"
    assert res != item


def test_code(tmpdir: Path) -> None:
    item = Item(path=tmpdir / "code.md")
    md = dedent(
        """
        # abcd

        ```python
        print("m00")
        ```

        ```c
        exit(EXIT_SUCCESS);
        ```

        ```
        asdf
        ```

        ```foobarbazqux
        hmm
        ```
        """
    )
    item.path.write_text(md)

    content = run(item).content
    assert content.count("highlight") == 2
    assert content.count("exit") == 1
    assert content.count("hmm") == 1
