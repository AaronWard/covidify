# -*- coding: utf-8 -*-
"""
    Setup file for covidify.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 3.2.2.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
import sys
import os
import re
from pkg_resources import VersionConflict, require
from setuptools import setup

try:
    require('setuptools>=38.3')
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)
    
def get_deps():    
    default = open('requirements.txt', 'r').readlines()
    new_pkgs = []
    for pkg in default:
        new_pkgs.append(pkg.strip())
    return new_pkgs

if __name__ == "__main__":
    setup(use_pyscaffold=True,
          package_data={
              '': ['*.txt', '*.csv', '*.yaml', '*.yml']
          },
          install_requires=get_deps()
         )