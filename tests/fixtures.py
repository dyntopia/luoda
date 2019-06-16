# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from os import chdir, getcwd
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator

from pytest import fixture


@fixture
def tmpdir() -> Iterator[Path]:
    orig = getcwd()

    with TemporaryDirectory() as tmp:
        chdir(tmp)
        yield Path(tmp)

    chdir(orig)
