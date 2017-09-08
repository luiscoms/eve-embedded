#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
from os.path import abspath, dirname, join
from eve_embedded import __version__


def read_file(filename):
    """Read the contents of a file located relative to setup.py"""
    with open(join(abspath(dirname(__file__)), filename)) as the_file:
        return the_file.read()


setuptools.setup(
    name="Eve-Embedded",
    version=__version__,
    description="Python project",
    url="https://github.com/luiscoms/eve-embedded",
    author="Luis Fernando Gomes",
    author_email="luiscoms@ateliedocodigo.com.br",
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    keywords=["eve", "rest", "api"],
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "eve",
        "requests"
    ],
    tests_require=["httpretty"],
    zip_safe=False,
)
