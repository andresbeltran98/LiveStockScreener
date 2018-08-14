#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for screener.

    This file was generated with PyScaffold 3.0.3.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: http://pyscaffold.org/
"""

import sys
from setuptools import setup, find_packages

# Add here console scripts and other entry points in ini-style format
# script_name = screener.module:function
entry_points = {
    'console_scripts': [
        'screener = screener.main:run'
    ]
}


dependencies = ['alabaster==0.7.11', 'Babel==2.6.0', 'certifi==2018.4.16',
                'chardet==3.0.4', 'cycler==0.10.0', 'docutils==0.14',
                'idna==2.7', 'imagesize==1.0.0', 'Jinja2==2.10',
                'kiwisolver==1.0.1', 'MarkupSafe==1.0', 'matplotlib==2.2.2',
                'mpl-finance==0.10.0', 'numpy==1.15.0', 'packaging==17.1',
                'pandas==0.23.4', 'Pygments==2.2.0', 'pyparsing==2.2.0',
                'python-dateutil==2.7.3', 'pytz==2018.5', 'requests==2.19.1',
                'six==1.11.0', 'snowballstemmer==1.2.1', 'urllib3==1.23']


def setup_package():
    needs_sphinx = {'build_sphinx', 'upload_docs'}.intersection(sys.argv)
    sphinx = ['sphinx'] if needs_sphinx else []
    setup(
        name='STOCK SCREENER',
        version='1.0',
        description='A live intraday stock screener',
        author='Andres Beltran',
        author_email='andresbeltran19@hotmail.com',
        license='MIT',
        packages=find_packages(exclude=['tests', 'tests.*']),
        install_requires=dependencies,
        # dependency_links=['https://github.com/matplotlib/mpl_finance'],
        setup_requires=['pyscaffold>=3.0a0,<3.1a0'] + sphinx,
        use_pyscaffold=True,
        entry_points=entry_points,
    )


if __name__ == "__main__":
    setup_package()
