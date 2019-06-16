# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from typing import IO, Any, Dict, cast

import toml
from voluptuous import Invalid, Optional, Required, Schema


class ConfigError(Exception):
    pass


schema = Schema({
    Required("build"): {
        Optional("template-dir", default="templates"): str,
        Optional("build-dir", default="build"): str,
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


def read(f: IO[str]) -> Dict[str, Any]:
    """
    Read and validate a TOML configuration.
    """
    try:
        return cast(Dict[str, Any], schema(toml.load(f)))
    except Invalid as e:
        msg = e.error_message
        path = ".".join((str(p) for p in e.path))
        raise ConfigError("{}: {}".format(msg, path))
