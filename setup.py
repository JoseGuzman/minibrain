"""
setup.py

Created: Sun Jun 30 15:16:05 CEST 2019

Installation file required for the minibrain module
"""
import os
import re
import os.path as op
from setuptools import setup 

#-------------------------------------------------------------------------
# setup
#-------------------------------------------------------------------------
def _package_tree(pkgroot):
    path = op.dirname(__file__)
    subdirs = [op.relpath(i[0], path).replace(op.sep, '.')
               for i in os.walk(op.join(path, pkgroot))
               if '__init__.py' in i[2]]
    return subdirs


# read README.md
curdir = op.dirname(op.realpath(__file__))
with open(op.join(curdir, 'README.md')) as f:
    myreadme = f.read()

# Find version number from `__init__.py` without executing it.
filename = op.join(curdir, 'minibrain/__init__.py')
with open(filename, 'r') as f:
    myversion = re.search(r"__version__ = '([^']+)'", f.read()).group(1)


setup(
    name = 'minibrain', # application name
    version = myversion,# application version
    license = 'LICENSE',
    description = 'minibrain analysis module',
    long_description = myreadme,
    author ='Jose Guzman',
    author_email = 'jguzman at guzman-lab.com',
    url = 'https://github.com/JoseGuzman/minibrain.git',
    packages = ['minibrain'],
    python_requires='>=2.7',
    include_package_data = True,# include additional data
    package_data={
        # If any package contains *.txt files, include them:
        '': ['*.txt'],
        # And include any *.syn files found in the 'data' subdirectory
        # of the 'minibrain' package, also:
        'minibrain': ['data/*.syn'],
    },
)
