#!/usr/bin/env python

from setuptools import setup

setup(
    name='cookbook',
    version='1.0',
    description='A place to store recipes',
    author='Mateusz Bocian',
    author_email='mateusz.bocian@mail.utoronto.ca',
    url='http://mrstork.github.io/',
    install_requires=[
        'Django==1.8.4'
    ],
    dependency_links=[
        'https://pypi.python.org/simple/django/'
    ],
)
