# pylint: disable=W0621
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path
from time import time

from dulwich.repo import Repo

from luoda.item import Item
from luoda.plugins.metadata import available, run

from ..fixtures import tmpdir  # pylint: disable=W0611


def test_available() -> None:
    assert available()


def test_without_git(tmpdir: Path) -> None:
    path = tmpdir / "foo"
    path.touch()

    item = Item(path=path)
    new_item = run(item)

    assert new_item.author == item.author
    assert new_item.file_date == item.file_date
    assert new_item.mtime != item.mtime


def test_with_git_in_cwd(tmpdir: Path) -> None:  # pylint: disable=W0613
    repo = Repo.init(".")

    item = Item(path=Path("src") / "foo")
    item.path.parent.mkdir()
    item.path.touch()

    # before commit
    new_item = run(item)
    assert new_item.author == item.author
    assert new_item.file_date == item.file_date
    assert new_item.mtime != item.mtime

    # after commit
    repo.stage([str(item.path)])

    timestamp = int(time())
    repo.do_commit(
        message=b"msg",
        committer=b"foo <a@b>",
        author=b"bar <x@y>",
        author_timestamp=timestamp,
    )

    new_item = run(item)
    assert new_item.author == "bar"
    assert new_item.file_date == timestamp
    assert new_item.mtime != item.mtime


def test_with_git_in_subdir(tmpdir: Path) -> None:
    repodir = tmpdir / "some" / "subdir"
    repodir.mkdir(parents=True)

    repo = Repo.init(str(repodir))

    item = Item(path=repodir / "xyz")
    item.path.touch()

    # before commit
    new_item = run(item)
    assert new_item.author == item.author
    assert new_item.file_date == item.file_date
    assert new_item.mtime != item.mtime

    # after commit
    repo.stage([item.path.name])

    timestamp = int(time())
    repo.do_commit(
        message=b"msg",
        committer=b"foo <a@b>",
        author=b"foo bar baz <x@y>",
        author_timestamp=timestamp,
    )

    new_item = run(item)
    assert new_item.author == "foo bar baz"
    assert new_item.file_date == timestamp
    assert new_item.mtime != item.mtime
