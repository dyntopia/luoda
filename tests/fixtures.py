# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from os import chdir, getcwd
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import IO, Iterator

from pytest import fixture


@fixture
def tmpfile() -> Iterator[IO[str]]:
    with NamedTemporaryFile("w+", buffering=1) as tmp:
        yield tmp


@fixture
def tmpdir() -> Iterator[Path]:
    orig = getcwd()

    with TemporaryDirectory() as tmp:
        chdir(tmp)
        yield Path(tmp)

    chdir(orig)
