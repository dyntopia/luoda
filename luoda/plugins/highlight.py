# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Plugin that writes pygments style files.

The actual pygments markup is generated in the file reader plugins.
"""

from typing import Any, Dict

from pygments.formatters.html import HtmlFormatter


def available() -> bool:
    return True


def run(item: Any, config: Dict[str, Any], **_kwargs: Any) -> Any:
    style = config["build"]["highlight"]
    output = config["build"]["build-dir"] / "static" / "highlight.css"

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(HtmlFormatter(style=style).get_style_defs())
    return item
