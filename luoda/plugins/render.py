# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Plugin that renders content with jinja2.
"""

from typing import Any, Dict, List

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
    autoescape = select_autoescape()
    loader = FileSystemLoader(str(config["build"]["template-dir"]))
    env = Sandbox(autoescape=autoescape, loader=loader)

    try:
        template = env.get_template(item.template)
        content = template.render(item=item, items=items, **config)
        return evolve(item, content=content)
    except TemplateError as e:
        print("ERROR: {}: {}".format(repr(e), e))
    return item
