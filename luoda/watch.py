# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from typing import Any, Callable, Optional

from livereload.watcher import Watcher, logger


class Watch(Watcher):
    _upcoming_tasks = {}  # type: dict

    def watch(
            self,
            path: str,
            func: Optional[Callable] = None,
            delay: int = 0,
            ignore: Optional[Callable] = None,
    ) -> None:
        """
        Watch a path.

        The watch is delayed until the next task examination to allow
        watchers to be added during the execution of `func`.
        """
        if callable(func) and not hasattr(func, "repr_str"):
            setattr(func, "repr_str", func.__name__)

        if path not in self._tasks:
            self._upcoming_tasks[path] = {
                "func": func,
                "delay": delay,
                "ignore": ignore
            }

    def examine(self) -> Any:
        for path in list(self._upcoming_tasks.keys()):
            logger.info("Watching %s", path)
            super().watch(path, **self._upcoming_tasks.pop(path))
        return super().examine()
