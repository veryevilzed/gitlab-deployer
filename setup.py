#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='deployer',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click', 'requests', 'python-gitlab'
    ],
    entry_points='''
        [console_scripts]
        deployer=deployer.main:cli
    ''',
)
