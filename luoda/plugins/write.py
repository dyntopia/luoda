# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Plugin that writes content to disk.

Filenames are transformed such that:

src/xyz/index.md -> dst/xyz/index.html
src/xyz/name.md -> dst/xyz/name/index.html
src/xyz/foo.svg -> dst/xyz/foo.svg
"""

from typing import Any, Dict


def available() -> bool:
    return True


def run(item: Any, config: Dict[str, Any], **_kwargs: Any) -> Any:
    src = item.path
    cd = config["build"]["collection-dir"]
    bd = config["build"]["build-dir"] / str(src)[len(str(cd)) + 1:]

    if isinstance(item.content, str):
        dst = (
            bd.with_suffix(".html") if bd.with_suffix("").name == "index" else
            bd.with_suffix("") / "index.html"
        )
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(item.content)
    else:
        dst = bd
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(item.content)

    return item
