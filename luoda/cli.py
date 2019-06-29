# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path
from typing import Any, Dict, Optional

import click
from livereload import Server
from livereload.watcher import logger

from . import config, pipeline, watch


@click.group()
@click.option(
    "--config-file",
    "-c",
    default=("config.toml"),
    show_default=True,
    type=click.Path(exists=True, dir_okay=False),
)
@click.pass_context
def cli(ctx: click.Context, config_file: str) -> None:
    ctx.obj = {"config": Path(config_file)}


@cli.command()
@click.pass_context
def build(ctx: click.Context) -> None:
    try:
        pipeline.build(ctx.obj["config"])
    except (config.ConfigError, pipeline.PipelineError) as e:
        raise click.ClickException(str(e))


@cli.command()
@click.pass_context
def serve(ctx: click.Context) -> None:
    watcher = watch.Watch()
    server = Server(watcher=watcher)

    def builder() -> Optional[Dict[str, Any]]:
        try:
            c = config.read(ctx.obj["config"])
            watcher.watch(str(ctx.obj["config"]), func=builder)
            watcher.watch(str(c["build"]["collection-dir"]), func=builder)
            watcher.watch(str(c["build"]["template-dir"]), func=builder)
            pipeline.build(ctx.obj["config"])
            return c
        except (config.ConfigError, pipeline.PipelineError) as e:
            logger.error("Error: %s", e)
        return None

    c = builder()
    if c:
        server.serve(
            host=c["serve"]["host"],
            port=c["serve"]["port"],
            root=str(c["build"]["build-dir"])
        )
