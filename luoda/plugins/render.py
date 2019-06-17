# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Plugin that renders content with jinja2.
"""

from datetime import date
from typing import Any, Dict, List, Union

from attr import evolve
from jinja2 import FileSystemLoader, select_autoescape
from jinja2.exceptions import TemplateError
from jinja2.sandbox import ImmutableSandboxedEnvironment


class Sandbox(ImmutableSandboxedEnvironment):
    def is_safe_callable(self, obj: object) -> bool:
        return False


def available() -> bool:
    return True


def run(item: Any, items: List[Any], config: Dict[str, Any]) -> Any:
    if item.template:
        autoescape = select_autoescape()
        loader = FileSystemLoader(str(config["build"]["template-dir"]))
        env = Sandbox(autoescape=autoescape, loader=loader)
        env.filters["strftime"] = _strftime

        try:
            template = env.get_template(item.template)
            content = template.render(item=item, items=items, **config)
            return evolve(item, content=content)
        except TemplateError as e:
            print("ERROR: {}: {}".format(repr(e), e))
    return item


def _strftime(timestamp: Union[int, float], fmt: str = "%Y-%m-%d") -> str:
    if not isinstance(timestamp, (int, float)) or not isinstance(fmt, str):
        raise TemplateError("invalid strftime() invocation")
    return date.fromtimestamp(timestamp).strftime(fmt)
