# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Plugin that prints the current state.
"""

from typing import Any


def available() -> bool:
    return True


def run(state: Any, *args: Any, **kwargs: Any) -> Any:
    print("state: {}, args: {}, kwargs: {}".format(state, args, kwargs))
    return state
