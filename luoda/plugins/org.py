# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Plugin that reads org-mode files.

This plugin also sets the author, date and title if available.
"""

import re
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
        title = soup.select_one("h1") or soup.select_one("h2")
        if title:
            title.extract()

        # `org-html--build-meta-info' uses bogus titles to avoid invalid
        # elements.
        bogus = [
            " *temp*",  # emacs24
            "\u200e",  # emacs26
        ]

        highlight(soup)
        insert_refs(soup)
        strip_js(soup)

        return evolve(
            item,
            content=str(content) if content else "",
            author=author.get("content") if author else "",
            file_date=parse_date(date.text.split()[-1]) if date else 0.0,
            title=title.text if title and title.text not in bogus else "",
        )
    return item


def parse_date(date: str) -> float:
    try:
        return mktime(strptime(date, "%Y-%m-%d"))
    except ValueError as e:
        raise PluginError(e)


def highlight(soup: BeautifulSoup) -> None:
    """
    Highlight source code blocks.
    """
    for src in soup.select("pre.src"):
        lang = [
            x.replace("src-", "")
            for x in src.attrs["class"]
            if x.startswith("src-")
        ][0]
        markup = BeautifulSoup(colorize(src.text, lang), "html.parser")
        src.replace_with(markup)


def insert_refs(soup: BeautifulSoup) -> None:
    """
    Insert code references.

    Org-mode is capable of referencing parts of code blocks, e.g.:

    #+BEGIN_SRC python
    ...
    print("hi")  # (ref:1)   -> <span id="coderef-1">
    ...
    #+END_SRC
    See [[(1)]]            -> <a href="coderef-1">

    However, the target <span> breaks when pygments transform code
    blocks.  This function re-inserts the targets for code references.
    """
    pat = re.compile(r" \(([0-9])+\)$")
    for ref in soup.find_all("span", class_="c1", text=pat):
        match = pat.search(ref.text)
        ref.attrs["id"] = "coderef-{}".format(match.group(1) if match else 0)


def strip_js(soup: BeautifulSoup) -> None:
    """
    Strip JavaScript attributes.

    Org-mode inserts code references like so:

    <a href=#coderef-1
       class="coderef"
       onmouseout="CodeHighlightOn(...);"
       onmouseover="CodeHighlightOff(...);">

    The `onmouseout` and `onmouseover` attributes are hardcoded in
    org-mode (see `org-html-link`).  Org-mode exports the JavaScript
    implementations for those events in <head>.  Since this plugin only
    extracts the content, browser errors arise if they aren't removed.
    """
    attrs = {"onmouseover", "onmouseout"}
    for tag in soup.find_all(lambda t: attrs.intersection(t.attrs)):
        tag.attrs = {k: v for k, v in tag.attrs.items() if k not in attrs}
