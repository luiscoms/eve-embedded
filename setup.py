#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
from setuptools.command.test import test as TestCommand  # noqa N812

from eve_embedded import __version__


class Tox(TestCommand):
    """Integration of tox via the setuptools ``test`` command"""
    # pylint: disable=attribute-defined-outside-init
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        from tox import cmdline  # pylint: disable=import-error
        args = self.tox_args
        if args:
            args = split(self.tox_args)
        cmdline(args=args)

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
    # setup_requires=[
    #     "requests",
    # ],
    # install_requires=[
    #     "eve",
    # ],
    # tests_require=['tox'],
    cmdclass={
        'test': Tox,
    },
    zip_safe=False,
)
