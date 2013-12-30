#!/usr/bin/env python

from setuptools import setup

import sys
sys.path.insert(0, '.')

from signup import __version__, __author__, __author_email__, __license__

NAME = "zabtman"
SHORT_DESC = "Template import/export manager for Zabbix 2+ using a git repository"


if __name__ == "__main__":
 
    setup(
        name = NAME,
        version = __version__,
        author = __author__,
        author_email = __author_email__,
        url = "https://github.com/gregswift/{0}".format(NAME),
        license = __license__,
        packages = [NAME],
        package_dir = {NAME: NAME},
        description = SHORT_DESC,
        install_requires = ['requests'],
        entry_points={
            'console_scripts': [ 'zabtman = zabtman.cli:run' ],
        }
    )
