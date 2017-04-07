#!/usr/bin/env python

from setuptools import setup

setup(
    name='Ryorisho',
    version='1.0',
    description='Share recipes and discover new ones',
    author='Mateusz Bocian',
    author_email='support@ryorisho.com',
    url='http://mrstork.github.io/',
    install_requires=[
        'Django==1.11'
    ],
    dependency_links=[
        'https://pypi.python.org/simple/django/'
    ],
)
