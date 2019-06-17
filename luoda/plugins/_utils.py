# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from typing import cast

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound


def colorize(code: str, lang: str) -> str:
    try:
        lexer = get_lexer_by_name(lang)
    except ClassNotFound:
        return code

    formatter = HtmlFormatter()
    return cast(str, highlight(code=code, lexer=lexer, formatter=formatter))
