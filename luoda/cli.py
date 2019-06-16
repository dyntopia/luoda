# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from typing import IO

import click

from . import config, pipeline


@click.group()
@click.option(
    "--config-file",
    "-c",
    default=("config.toml"),
    show_default=True,
    type=click.File("r"),
)
@click.pass_context
def cli(ctx: click.Context, config_file: IO) -> None:
    try:
        ctx.obj = {"config": config.read(config_file)}
    except config.ConfigError as e:
        raise click.ClickException("{}: {}".format(config_file.name, e))


@cli.command()
@click.pass_context
def build(ctx: click.Context) -> None:
    try:
        pipeline.build(ctx.obj["config"])
    except pipeline.PipelineError as e:
        raise click.ClickException(str(e))
