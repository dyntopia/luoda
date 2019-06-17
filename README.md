![Build](https://img.shields.io/travis/dyntopia/luoda.svg)
![Coverage](https://img.shields.io/codecov/c/github/dyntopia/luoda.svg)

luoda
=====

About
-----

`luoda` is a plugin-based static site generator.  It ships with the
following plugins:

- `org` - Reads org-mode files with `emacs` if it's installed.  Code
  blocks are highlighted with pygments [5].
- `markdown` - Reads markdown files with mistune [1].  Code blocks are
  highlighted with pygments [5].
- `static` - Reads files as-is.
- `metadata` - Retrieves `author` and `date` from git repositories with
  dulwich [2].  It also sets `mtime`.
- `render` - Renders parsed content with the jinja2 [3] template engine.
- `minimize` - Minimize rendered HTML content with htmlmin [4].
- `write` - Writes content to disk.
- `tap` - Helper that prints the current state.


Usage
-----

To build the site:

```sh
$ luoda build
```


Configuration
-------------

A simple configuration file looks as follows:

```toml
[build]
# Required: source directory for jinja2 templates.
template-dir = "templates"

# Required: top-level directory for the collections to build.
collection-dir = "collections"

# Optional: output directory.
build-dir = "build"

# Required: plugins to use.  Order is important!
plugins = [
    "metadata",
    "markdown",
    "static",
    "render",
    "minimize",
    "write"
]

[site]
# Optional: name if the site
name = "luoda"

[[collection]]
# Required: name of the collection
name = "blog-posts"

# Optional: name of the template to use.  Files are read as-is if no
# template is provided and if the `static` module is enabled.
template = "post.html"

# Required: list of globs to include for this collection, relative to
# collection-dir
paths = ["blog/**.md"]

# Optional: list of globs to exclude from `paths`, relative to
# collection-dir
ignore-paths = ["blog/index.md"]

[[collection]]
# Required: name of the collection
name = "blog-index"

# Optional: name of the template to use.  Files are read as-is if no
# template is provided and if the `static` module is enabled.
template = "list.html"

# Required: list of globs to include for this collection, relative to
# collection-dir
paths = ["blog/index.md"]
```


[1]: https://pypi.org/project/mistune/
[2]: https://pypi.org/project/dulwich/
[3]: https://pypi.org/project/jinja2/
[4]: https://pypi.org/project/htmlmin/
[5]: https://pypi.org/project/pygments/
