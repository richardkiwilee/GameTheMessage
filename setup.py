#!/usr/bin/env python
from setuptools import setup, find_packages

name = 'GameTheMessage'
description = 'Custom game GameTheMessage, a self-made desktop game, inspired by the game "Attack by Stratagem".'

with open('requirements.txt', 'r') as f:
    requires = [line.rstrip() for line in f.readlines()]


def get_version():
    u""" 从__version__.py中读取版本号。 """
    with open('GameTheMessage/__version__.py') as version_file:
        for line in version_file:
            if line.startswith('__version__'):
                # pylint: disable=eval-used
                return eval(line.split('=')[-1])


setup(
    name=name,
    version=get_version(),
    description=description,
    packages=find_packages(),
    package_data={},
    entry_points={'console_scripts': ['GameTheMessage = GameTheMessage.cli:main']},
    zip_safe=False,
    include_package_data=True,
    install_requires=requires,
    platforms='any',
    url=None,
    author='Richard Kiwi Lee',
)
