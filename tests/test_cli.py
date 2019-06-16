# pylint: disable=W0621
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from typing import Callable, Iterator, cast

import click
import click.testing
import toml
from pytest import fixture
from pytest_mock import MockFixture

from luoda.cli import cli
from luoda.config import schema


@cast(Callable[[Callable], Iterator[Callable]], fixture)
def invoke() -> Iterator[Callable]:
    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        yield lambda *args, **kwargs: runner.invoke(cli, *args, **kwargs)


def test_missing_config(invoke: Callable) -> None:
    @cli.command()
    @click.pass_context
    def missing_config(_ctx: click.Context) -> None:  # pylint: disable=W0612
        pass

    r = invoke("missing-config")
    assert r.output.index("Could not open file")
    assert r.exit_code != 1


def test_invalid_config(invoke: Callable) -> None:
    config = {"build": {}, "site": {}}  # type: dict

    @cli.command()
    def invalid_config() -> None:  # pylint: disable=W0612
        pass

    with open("config", "w") as f:
        toml.dump(config, f)

    r = invoke("--config-file config invalid-config")
    assert r.output.index("required key not provided: collections")
    assert r.exit_code != 0


def test_valid_config(invoke: Callable) -> None:
    config = {"build": {}, "site": {}, "collections": []}  # type: dict

    @cli.command()
    @click.pass_context
    def valid_config(ctx: click.Context) -> None:  # pylint: disable=W0612
        assert ctx.obj["config"] == schema(config)

    with open("config", "w") as f:
        toml.dump(config, f)

    r = invoke("--config-file config valid-config")
    assert r.exit_code == 0

    r = invoke("-c config valid-config")
    assert r.exit_code == 0


def test_failed_build(invoke: Callable) -> None:
    config = {
        "build": {
            "plugins": ["foo"]
        },
        "site": {},
        "collections": [],
    }  # type: dict

    with open("config", "w") as f:
        toml.dump(config, f)

    r = invoke("-c config build")
    assert r.output.index("unknown plugin(s): foo")
    assert r.exit_code != 0


def test_successful_build(invoke: Callable, mocker: MockFixture) -> None:
    config = {"build": {}, "site": {}, "collections": []}  # type: dict

    with open("config", "w") as f:
        toml.dump(config, f)

    build = mocker.patch("luoda.pipeline.build")
    invoke("-c config build")
    build.assert_called_once_with(schema(config))
