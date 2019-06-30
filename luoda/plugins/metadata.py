# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Plugin that parses metadata.

The `mtime` property in `item` is always set.  The `author` and `date`
properties are set if the file is in a git repository.
"""

import re
from pathlib import Path
from typing import Any, Optional

from attr import evolve
from dulwich.repo import Repo


def available() -> bool:
    return True


def run(item: Any, **_kwargs: Any) -> Any:
    stat = item.path.stat()
    item = evolve(item, mtime=stat.st_mtime)

    git = find_git(item.path)
    if git:
        repo = Repo(git)
        relpath = Path(str(item.path)[len(git) + 1 if git != "." else 0:])
        try:
            walker = repo.get_walker(paths=[bytes(relpath)], follow=True)
            commit = next(iter(walker)).commit
            item = evolve(
                item,
                author=re.sub(" <.*", "", commit.author.decode()),
                file_date=commit.author_time,
            )
        except (KeyError, StopIteration):
            pass

    return item


def find_git(path: Optional[Path]) -> Optional[str]:
    while path:
        if (path / ".git").is_dir():
            return str(path)
        path = path.parent if not path == path.parent else None
    return None
