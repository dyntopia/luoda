# pylint: disable=W0212
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from luoda.watch import Watch


def test_watch() -> None:
    w = Watch()
    w.watch("foo")

    assert "foo" in w._upcoming_tasks
    assert "foo" not in w._tasks

    w.examine()

    assert "foo" not in w._upcoming_tasks
    assert "foo" in w._tasks

    w.watch("foo")
    assert "foo" not in w._upcoming_tasks


def test_repr() -> None:
    w = Watch()
    w.watch("foo", func=test_repr)

    assert w._upcoming_tasks["foo"]["func"].repr_str == "test_repr"
