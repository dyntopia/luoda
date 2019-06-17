luoda
=====

About
-----

`luoda` is a plugin-based static site generator.  It ships with the
following plugins:

- `markdown` - Reads markdown files with mistune [1]
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

# Required: name of the template to use
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

# Required: name of the template to use
template = "list.html"

# Required: list of globs to include for this collection, relative to
# collection-dir
paths = ["blog/index.md"]
```


[1]: https://pypi.org/project/mistune/
[2]: https://pypi.org/project/dulwich/
[3]: https://pypi.org/project/jinja2/
[4]: https://pypi.org/project/htmlmin/
