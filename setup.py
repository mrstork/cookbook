#!/usr/bin/env python

from setuptools import setup

setup(
    name='kukkubu',
    version='1.0',
    description='A place to store your personal recipes',
    author='Mateusz Bocian',
    author_email='support@kukkubu.com',
    url='http://mrstork.github.io/',
    install_requires=[
        'Django==1.8.4'
    ],
    dependency_links=[
        'https://pypi.python.org/simple/django/'
    ],
)
