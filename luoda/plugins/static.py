# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Plugin that reads files with no parsing.
"""

from typing import Any

from attr import evolve

extensions = (
    ".css",
    ".gif"
    ".htm",
    ".html",
    ".jpeg",
    ".jpg",
    ".js",
    ".png",
    ".svg",
)


def available() -> bool:
    return True


def run(item: Any, **_kwargs: Any) -> Any:
    if not item.template and item.path.suffix.lower() in extensions:
        return evolve(item, content=item.path.read_bytes())
    return item
