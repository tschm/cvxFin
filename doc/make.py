#!/usr/bin/env python

"""
Python script for building documentation.

To build the docs you must have all optional dependencies for pandas
installed. See the installation instructions for a list of these.

Note: currently latex builds do not work because of table formats that are not
supported in the latex generation.

Usage
-----
python make.py clean
python make.py html
"""
#from __future__ import print_function

import os
import shutil
import sys

os.environ['PYTHONPATH'] = '..'

SPHINX_BUILD = 'sphinxbuild'


def clean():
    if os.path.exists('build'):
        shutil.rmtree('build')

    if os.path.exists('source/generated'):
        shutil.rmtree('source/generated')


def html():
    check_build()
    if os.system('sphinx-build -P -b html -d build/doctrees '
                 'source build/html'):
        raise SystemExit("Building HTML failed.")


def check_build():
    build_dirs = [
        'build', 'build/doctrees', 'build/html',
        'build/latex', 'build/plots', 'build/_static',
        'build/_templates']
    for d in build_dirs:
        try:
            os.mkdir(d)
        except OSError:
            pass


if __name__ == '__main__':
    clean()
    html()

