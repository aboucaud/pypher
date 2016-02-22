#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from setuptools import setup, find_packages


def find_version():
    """Find project version"""
    with open('make_psf_kernel.py') as pfile:
        version_file = pfile.read()
    try:
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                                  version_file, re.M)
        version = version_match.group(1)
    except AttributeError:
        version = 'Unknown'

    return version

setup(
    name='make_psf_kernel',
    author='Alexandre Boucaud',
    author_email='alexandre.boucaud@ias.u-psud.fr',
    maintainer='Alexandre Boucaud',
    maintainer_email='boucaud.alexandre@gmail.com',
    description='Compute an homogenization kernel between two PSF',
    license='New BSD',
    url='https://git.ias.u-psud.fr/aboucaud/make_psf_kernel/',
    download_url='https://git.ias.u-psud.fr/aboucaud/make_psf_kernel/',
    version=find_version(),
    long_description=open('README.md').read(),
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mk-kernel = make_psf_kernel:main',
        ],
    },
    install_requires=[
        'numpy >= 1.7.2',
        'scipy >= 0.9.0',
        'pyfits >= 3.2.0'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
