# pylint: disable=W0621
#
# Copyright (c) 2019, Hans Jerry Illikainen <hji@dyntopia.com>
#
# SPDX-License-Identifier: BSD-2-Clause

from os import mkdir
from pathlib import Path
from typing import Callable, Iterator

import click
import click.testing
import toml
from pytest import fixture
from pytest_mock import MockFixture

from luoda.cli import cli
from luoda.config import ConfigError, read, schema


@fixture
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
    assert r.output.index("does not exist")
    assert r.exit_code != 1


def test_invalid_config(invoke: Callable) -> None:
    config = {
        "build": {
            "collection-dir": "c",
            "template-dir": "t",
        },
    }  # type: dict

    mkdir("t")

    @cli.command()
    @click.pass_context
    def invalid_config(ctx: click.Context) -> None:  # pylint: disable=W0612
        try:
            read(ctx.obj["config"])
        except ConfigError as e:
            raise click.ClickException(str(e))

    with open("config", "w") as f:
        toml.dump(config, f)

    r = invoke("--config-file config invalid-config")
    assert r.output.index("not a directory")
    assert r.exit_code != 0


def test_valid_config(invoke: Callable) -> None:
    config = {
        "build": {
            "collection-dir": "c",
            "template-dir": "t",
        },
        "extra": {},
        "collections": []
    }  # type: dict

    mkdir("c")
    mkdir("t")

    @cli.command()
    @click.pass_context
    def valid_config(ctx: click.Context) -> None:  # pylint: disable=W0612
        assert read(ctx.obj["config"]) == schema(config)

    with open("config", "w") as f:
        toml.dump(config, f)

    r = invoke("--config-file config valid-config")
    assert r.exit_code == 0

    r = invoke("-c config valid-config")
    assert r.exit_code == 0


def test_failed_build(invoke: Callable) -> None:
    config = {
        "build": {
            "collection-dir": "c",
            "template-dir": "t",
            "plugins": ["foo"],
        },
        "extra": {},
        "collections": [],
    }  # type: dict

    mkdir("c")
    mkdir("t")

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
    build.assert_called_once_with(Path("config"))


def test_successful_serve(invoke: Callable, mocker: MockFixture) -> None:
    config = {
        "build": {
            "build-dir": "abcd",
        },
        "serve": {
            "host": "127.0.0.1",
            "port": 1234,
        }
    }
    with open("config", "w") as f:
        toml.dump(config, f)

    mkdir("collections")
    mkdir("templates")

    serve = mocker.patch("luoda.cli.Server.serve")
    invoke("-c config serve")
    serve.assert_called_once_with(host="127.0.0.1", port=1234, root="abcd")


def test_failed_serve(invoke: Callable, mocker: MockFixture) -> None:
    config = {
        "build": {
            "collection-dir": "does-not-exist",
        }
    }
    with open("config", "w") as f:
        toml.dump(config, f)

    serve = mocker.patch("luoda.cli.Server.serve")
    invoke("-c config serve")
    serve.assert_not_called()
