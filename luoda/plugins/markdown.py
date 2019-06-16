# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Plugin that reads markdown files.
"""

from typing import Any, Optional

from attr import evolve
from mistune import Markdown, Renderer


class Render(Renderer):
    title = ""

    def header(self, text: str, level: int, raw: Optional[str] = None) -> Any:
        if level == 1:
            self.title = text
        return super().header(text, level, raw)


def available() -> bool:
    return True


def run(item: Any, **_kwargs: Any) -> Any:
    if item.path.suffix.lower() == ".md":
        renderer = Render(escape=True)
        markdown = Markdown(renderer=renderer)
        content = markdown(item.path.read_text())
        item = evolve(item, content=content, title=renderer.title)
    return item
