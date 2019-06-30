# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path
from typing import Union

from attr import attrib, attrs


@attrs(frozen=True, kw_only=True)
class Item:
    author = attrib(type=str, default="")
    content = attrib(type=Union[bytes, str], default="")
    file_date = attrib(type=float, default=0.0)
    file_mtime = attrib(type=float, default=0.0)
    keywords = attrib(type=str, default="")
    path = attrib(type=Path)
    template = attrib(type=str, default="")
    title = attrib(type=str, default="")
