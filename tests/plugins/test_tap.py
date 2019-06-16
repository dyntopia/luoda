# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pytest_mock import MockFixture

from luoda.plugins.tap import available, run


def test_available() -> None:
    assert available()


def test_run(mocker: MockFixture) -> None:
    p = mocker.patch("luoda.plugins.tap.print")
    run("abcd", [1, 2, 3], foo="bar")
    assert p.call_count == 1
