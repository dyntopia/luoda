# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from pathlib import Path

import click

from . import config, pipeline


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
