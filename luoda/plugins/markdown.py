# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Plugin that reads markdown files.
"""

from typing import Any, Optional, cast

from attr import evolve
from mistune import Markdown, Renderer

from ._utils import colorize


class Render(Renderer):
    title = ""

    def header(self, text: str, level: int, raw: Optional[str] = None) -> str:
        if level == 1:
            self.title = text
            return ""
        return cast(str, super().header(text, level, raw))

    def block_code(self, code: str, lang: Optional[str] = None) -> str:
        if lang:
            return colorize(code, lang)
        return cast(str, super().block_code(code, lang))


def available() -> bool:
    return True


def run(item: Any, **_kwargs: Any) -> Any:
    if item.path.suffix.lower() == ".md":
        renderer = Render(escape=True)
        markdown = Markdown(renderer=renderer)
        content = markdown(item.path.read_text())
        item = evolve(item, content=content, title=renderer.title)
    return item
