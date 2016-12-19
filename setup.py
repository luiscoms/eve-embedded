#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

from eve_embedded import __version__

setuptools.setup(
    name="Eve-Embedded",
    version=__version__,
    description="Python boilerplate project",
    url="https://github.com/westphahl/boilerplate",
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
    install_requires=[],
    entry_points={
        "console_scripts": [
            "boilerplate_script = boilerplate.script:main"
        ]
    }
)
