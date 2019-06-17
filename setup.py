#!/usr/bin/env python3

from setuptools import setup

import luoda

setup(
    name=luoda.__project__,
    version=luoda.__version__,
    author="Hans Jerry Illikainen",
    author_email="hji@dyntopia.com",
    license="BSD-2-Clause",
    description="Static site generator",
    long_description="See https://github.com/dyntopia/luoda",
    url="https://github.com/dyntopia/luoda",
    python_requires=">=3.5",
    entry_points={
        "console_scripts": ["luoda = luoda.__main__:main"],
    },
    packages=[
        "luoda",
        "luoda.plugins",
    ],
    install_requires=[
        "attrs",
        "click",
        "dulwich",
        "htmlmin",
        "jinja2",
        "livereload",
        "pluginbase",
        "toml",
        "voluptuous",
    ],
    tests_requires=[
        "coverage",
        "isort",
        "mccabe",
        "mypy",
        "ossaudit",
        "pycodestyle",
        "pyflakes",
        "pylint",
        "pylint-quotes",
        "pytest",
        "pytest-mock",
        "safety",
        "yapf",
    ],
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
)
