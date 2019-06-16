# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from itertools import chain
from pathlib import Path
from typing import Iterable


def flatten(iterable: Iterable) -> Iterable:
    """
    Flatten `iterable` by one level of nesting.
    """
    return chain.from_iterable(iterable)


def lglobs(globs: Iterable[str]) -> Iterable[Path]:
    """
    Retrieve paths for the elements in `globs`.
    """
    return flatten([Path(".").glob(g) for g in globs])
