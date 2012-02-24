#!/usr/bin/env python
import os
from setuptools import setup, find_packages

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   'README.rst')
dependencies = [
    'django',
    'south',
]

setup(
    name='powwow',
    version='0.1',
    description='Productivity apps built around Google+ Hangouts API.',
    long_description = open(README_PATH, 'r').read(),
    author='Angel Ramboi',
    author_email='angel.ramboi@gmail.com',
    url='https://github.com/pbs/powwow',
    packages=find_packages(),
    include_package_data=True,
    install_requires=dependencies,
    license='New BSD License',
)
