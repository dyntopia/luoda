# pylint: disable=C0102,W0621
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path
from time import sleep, time

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
    assert new_item.dir_date == item.dir_date
    assert new_item.file_mtime != item.file_mtime
    assert new_item.dir_mtime != item.dir_mtime


def test_with_git_in_cwd(tmpdir: Path) -> None:  # pylint: disable=W0613
    repo = Repo.init(".")

    item = Item(path=Path("src") / "foo")
    item.path.parent.mkdir()
    item.path.touch()

    # before commit
    new_item = run(item)
    assert new_item.author == item.author
    assert new_item.file_date == item.file_date
    assert new_item.dir_date == item.dir_date
    assert new_item.file_mtime != item.file_mtime
    assert new_item.dir_mtime != item.dir_mtime

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
    assert new_item.dir_date == timestamp
    assert new_item.file_mtime != item.file_mtime
    assert new_item.dir_mtime != item.dir_mtime


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
    assert new_item.dir_date == item.dir_date
    assert new_item.file_mtime != item.file_mtime

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
    assert new_item.dir_date == timestamp
    assert new_item.file_mtime != item.file_mtime
    assert new_item.dir_mtime != item.dir_mtime


def test_date(tmpdir: Path) -> None:  # pylint: disable=W0613
    repo = Repo.init(".")

    parent = Path("src")
    parent.mkdir()

    foo = parent / "foo"
    bar = parent / "bar"

    foo.touch()
    bar.touch()

    timestamp = int(time())

    repo.stage([str(foo)])
    repo.do_commit(
        message=b"msg",
        committer=b"foo <a@b>",
        author=b"bar <x@y>",
        author_timestamp=timestamp,
    )

    first = run(Item(path=foo))
    assert first.file_date == timestamp
    assert first.dir_date == timestamp

    repo.stage([str(bar)])
    repo.do_commit(
        message=b"msg",
        committer=b"foo <a@b>",
        author=b"bar <x@y>",
        author_timestamp=timestamp + 100,
    )

    second = run(Item(path=bar))
    assert second.file_date == timestamp + 100
    assert second.dir_date == timestamp


def test_mtime(tmpdir: Path) -> None:
    (tmpdir / "foo").touch()
    item = run(Item(path=tmpdir / "foo"))
    assert item.file_mtime == item.dir_mtime

    sleep(0.01)

    (tmpdir / "bar").touch()
    new_item = run(Item(path=tmpdir / "foo"))
    assert new_item.file_mtime < new_item.dir_mtime
