# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path
from typing import Any, Dict, cast

import toml
from voluptuous import Coerce, Invalid, Optional, Required, Schema


class ConfigError(Exception):
    pass


schema = Schema({
    Required("build"): {
        Optional("template-dir", default="templates"): Coerce(Path),
        Optional("build-dir", default="build"): Coerce(Path),
        Optional("highlight", default="default"): str,
        Required("plugins", default=[]): [str],
    },
    Required("site"): {
        Required("name", default="luoda"): str,
    },
    Required("collections"): [{
        Required("name"): str,
        Required("template"): str,
        Required("paths"): [str],
        Optional("ignore-paths", default=[]): [str],
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
