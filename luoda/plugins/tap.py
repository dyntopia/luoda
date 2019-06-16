# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Plugin that prints the current state.
"""

from pprint import pformat
from typing import Any


def available() -> bool:
    return True


def run(state: Any, *args: Any, **kwargs: Any) -> Any:
    pp = [pformat(x) for x in [state, args, kwargs]]
    print("{}\n - state: {}\n - args: {}\n - kwargs: {}".format("-" * 24, *pp))
    return state
