#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 IAS / CNRS / Univ. Paris-Sud
# BSD License - see attached LICENSE file
# Author: Alexandre Boucaud <alexandre.boucaud@ias.u-psud.fr>
from setuptools import setup, find_packages


def find_version(filepath):
    """
    Find project version in a given file

    The syntax for the file version need to be in the form
    __version__ = 'a.b.c'
    which follows the semantic versioning http://semver.org/
    * a : major version
    * b : minor version
    * c : patch version

    Parameters
    ----------
    filepath: str
        Path to the file containing a version number

    Returns
    -------
    version: str
        The program version in the form 'a.b.c' as described above

    """
    with open(filepath) as pfile:
        for line in pfile.readlines():
            if line.startswith('__version__'):
                version = line.strip()[-6:-1]
    return version

setup(
    name='pypher',
    author='Alexandre Boucaud',
    author_email='alexandre.boucaud@ias.u-psud.fr',
    maintainer='Alexandre Boucaud',
    maintainer_email='boucaud.alexandre@gmail.com',
    description='Python-based PSF Homogenization kERnels production',
    license='New BSD',
    url='http://pypher.readthedocs.org/en/latest/',
    download_url='https://git.ias.u-psud.fr/aboucaud/pypher/',
    version=find_version('pypher/pypher.py'),
    long_description=open('README.rst').read(),
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pypher = pypher.pypher:main',
            'addpixscl = pypher.addpixscl:main',
        ],
    },
    install_requires=[
        'numpy>=1.7.2',
        'scipy>=0.9',
        'astropy>=0.4'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
