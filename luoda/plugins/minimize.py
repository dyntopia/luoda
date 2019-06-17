# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from typing import Any

from attr import evolve
from htmlmin import minify


def available() -> bool:
    return True


def run(item: Any, **_kwargs: Any) -> Any:
    content = minify(
        input=item.content,
        remove_comments=True,
        remove_empty_space=True,
        remove_all_empty_space=True,
        reduce_empty_attributes=True,
        reduce_boolean_attributes=True,
        remove_optional_attribute_quotes=True,
    )
    return evolve(item, content=content)
