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


def lglobs(
        path: Path,
        globs: Iterable[str],
        ignore_globs: Iterable[str],
) -> Iterable[Path]:
    """
    Retrieve the globs for each element in `globs` sans `ignore_globs`.
    """
    paths = flatten(path.glob(g) for g in globs)
    ignore_paths = flatten(path.glob(ig) for ig in ignore_globs)
    return set(paths).difference(ignore_paths)
