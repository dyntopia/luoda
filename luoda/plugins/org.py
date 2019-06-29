# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Plugin that reads org-mode files.

This plugin also sets the author, date and title if available.
"""

from pathlib import Path
from shutil import which
from subprocess import STDOUT, CalledProcessError, check_output
from time import mktime, strptime
from typing import Any

from attr import evolve
from bs4 import BeautifulSoup
from pkg_resources import resource_filename

from ._exceptions import PluginError
from ._utils import colorize


def available() -> bool:
    return which("emacs") is not None


def run(item: Any, **_kwargs: Any) -> Any:
    if item.path.suffix.lower() == ".org":
        el = Path(resource_filename("luoda", "data")) / "luoda-org-export.el"
        args = [
            "emacs",
            "--batch",
            "--quick",
            "--no-window-system",
            "--load",
            str(el),
            "--luoda-org-export",
            str(item.path),
        ]

        try:
            output = check_output(args, stderr=STDOUT)
        except CalledProcessError as e:
            raise PluginError("org: {}".format(e.output.decode()))

        soup = BeautifulSoup(output, features="html.parser")
        author = soup.select_one("meta[name=author]")
        content = soup.select_one("div#content")
        date = soup.select_one("p.date")
        title = soup.select_one("h1")
        if title:
            title.extract()

        # `org-html--build-meta-info' uses bogus titles to avoid invalid
        # elements.
        bogus = [
            " *temp*",  # emacs24
            "\u200e",  # emacs26
        ]

        for src in soup.select("pre.src"):
            lang = [
                x.replace("src-", "")
                for x in src.attrs["class"]
                if x.startswith("src-")
            ][0]
            markup = colorize(src.text, lang)
            src.replace_with(BeautifulSoup(markup, "html.parser"))

        return evolve(
            item,
            content=str(content) if content else "",
            author=author.get("content") if author else "",
            date=parse_date(date.text.split()[-1]) if date else 0.0,
            title=title.text if title and title.text not in bogus else "",
        )
    return item


def parse_date(date: str) -> float:
    try:
        return mktime(strptime(date, "%Y-%m-%d"))
    except ValueError as e:
        raise PluginError(e)
