# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from functools import reduce
from pathlib import Path
from typing import Any, Iterable, List, Optional

from pluginbase import PluginBase

from . import __project__
from .config import read
from .item import Item
from .utils import lglobs


class PipelineError(Exception):
    pass


class Pipeline(PluginBase):
    def __init__(self, package: str, searchpath: Optional[List[str]] = None):
        super().__init__(package=package, searchpath=searchpath)
        self._plugins = []  # type: List

    def load(self, plugins: Iterable[str]) -> None:
        """
        Load pipeline plugins.

        :param plugins: Plugins to load.  The default is to load every
            available plugin.
        """
        src = self.make_plugin_source(searchpath=self.searchpath, persist=True)

        diff = set(plugins).difference(
            p for p in src.list_plugins() if not p.startswith("_")
        )
        if diff:
            unknown = ", ".join(diff)
            raise PipelineError("unknown plugin(s): {}".format(unknown))

        self._plugins = [
            p for p in (src.load_plugin(name) for name in plugins)
            if p.available()
        ]

    def run(self, state: Any, *args: Any, **kwargs: Any) -> Any:
        """
        Execute every available plugin.

        :param state: Initial state for the first plugin.  Each plugin
            should return the next state (or the present state, if
            noting is done) for subsequent plugins.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        :returns: The final state.
        """
        return reduce(
            lambda s, p: p.run(s, *args, **kwargs),
            self._plugins,
            state,
        )


def build(config: Path) -> None:
    c = read(config)
    pipeline = Pipeline(__project__, [str(Path(__file__).parent / "plugins")])
    pipeline.load(c["build"]["plugins"])

    items = []  # type: List[Item]
    for collection in c["collections"]:
        template = collection["template"]
        paths = lglobs(
            c["build"]["collection-dir"],
            collection["paths"],
            collection["ignore-paths"],
        )

        for path in paths:
            print("building {}".format(path))
            item = Item(path=path, template=template)
            items.append(pipeline.run(item, items=items, config=c))
