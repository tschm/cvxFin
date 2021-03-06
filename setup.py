#!/usr/bin/env python

from setuptools import setup

setup(
    name='cvxFin',
    version='0.2.2',
    packages=['cvxFin'],
    url='https://github.com/tschm/cvxFin',
    author='Thomas Schmelzer',
    author_email='thomas.schmelzer@gmail.com',
    install_requires=['pandas>=0.25.3', 'cvxpy>=1.0.31']
)
