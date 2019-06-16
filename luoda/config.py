# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path
from typing import Any, Dict, cast

import toml
from voluptuous import All, Coerce, Invalid, IsDir, Required, Schema


class ConfigError(Exception):
    pass


Dir = Coerce(Path, "expected a directory")
ExistingDir = All(IsDir(None), Dir)

schema = Schema({
    Required("build"): {
        Required("build-dir", default="build"): Dir,
        Required("collection-dir", default="collections"): ExistingDir,
        Required("template-dir", default="templates"): ExistingDir,
        Required("highlight", default="default"): str,
        Required("plugins", default=[]): [str],
    },
    Required("site"): {
        Required("name", default="luoda"): str,
    },
    Required("collections"): [{
        Required("name"): str,
        Required("template"): str,
        Required("paths"): [str],
        Required("ignore-paths", default=[]): [str],
    }],
})


def read(path: Path) -> Dict[str, Any]:
    """
    Read and validate a TOML configuration.
    """
    try:
        return cast(Dict[str, Any], schema(toml.load(path)))
    except Invalid as e:
        msg = e.error_message
        paths = ".".join(str(p) for p in e.path)
        raise ConfigError("{}: {}".format(msg, paths))
